#!/usr/bin/env python3
"""Apply FloppyKernel-Zareth R5 5.x networking backports & Internet tunings to 4.14.357."""

import os
import shutil
import sys


def replace_once(path: str, old: str, new: str, label: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    count = data.count(old)
    assert count == 1, f"[{label}] Expected exactly 1 match in {path}, found {count}"
    data = data.replace(old, new, 1)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    print(f"  [OK] {label} -> {path}")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <kernel_dir> <backports_dir>")
        sys.exit(1)

    kdir = os.path.abspath(sys.argv[1])
    bdir = os.path.abspath(sys.argv[2])
    os.chdir(kdir)

    print("=== [1/4] Backporting Official Google BBRv2 (5.13 v2alpha) ===")
    shutil.copyfile(os.path.join(bdir, "tcp_bbr2.c"), os.path.join(kdir, "net/ipv4/tcp_bbr2.c"))
    shutil.copyfile(os.path.join(bdir, "tcp_dctcp.h"), os.path.join(kdir, "net/ipv4/tcp_dctcp.h"))

    # include/net/inet_connection_sock.h
    replace_once(
        "include/net/inet_connection_sock.h",
        "\tu64\t\t\t  icsk_ca_priv[88 / sizeof(u64)];\n#define ICSK_CA_PRIV_SIZE      (11 * sizeof(u64))",
        "\tu64\t\t\t  icsk_ca_priv[224 / sizeof(u64)];\n#define ICSK_CA_PRIV_SIZE      (28 * sizeof(u64))",
        "ICSK_CA_PRIV_SIZE 224B",
    )
    replace_once(
        "include/net/inet_connection_sock.h",
        "\tICSK_ACK_PUSHED = 4,\n\tICSK_ACK_PUSHED2 = 8\n};",
        "\tICSK_ACK_PUSHED = 4,\n\tICSK_ACK_PUSHED2 = 8,\n\tICSK_ACK_NOW = 16\t/* Send the next ACK immediately (once) */\n};",
        "ICSK_ACK_NOW",
    )

    # include/linux/tcp.h
    replace_once(
        "include/linux/tcp.h",
        "\tu8\ttlp_retrans:1,\t/* TLP is a retransmission */\n\t\tunused_1:7;",
        "\tu8\ttlp_retrans:1,\t/* TLP is a retransmission */\n\t\tfast_ack_mode:2, /* which fast ack mode ? */\n\t\tunused_1:5;",
        "tcp_sock.fast_ack_mode",
    )
    replace_once(
        "include/linux/tcp.h",
        "\tu64\ttcp_wstamp_ns;\t/* departure time for next sent data packet */",
        "\tu64\ttcp_wstamp_ns;\t/* departure time for next sent data packet */\n\tu64\ttcp_clock_cache; /* cache last tcp_clock_ns() */",
        "tcp_sock.tcp_clock_cache",
    )
    replace_once(
        "include/linux/tcp.h",
        "\tu32\tsnd_up;\t\t/* Urgent pointer\t\t*/",
        "\tu32\tsnd_up;\t\t/* Urgent pointer\t\t*/\n\tu32\treord_seen;\t/* number of data packet reordering events */",
        "tcp_sock.reord_seen",
    )

    # include/net/tcp.h
    replace_once(
        "include/net/tcp.h",
        "#define\tTCP_ECN_SEEN\t\t8\n",
        "#define\tTCP_ECN_SEEN\t\t8\n#define\tTCP_ECN_ECT_PERMANENT\t16\n",
        "TCP_ECN_ECT_PERMANENT",
    )
    replace_once(
        "include/net/tcp.h",
        "static inline u32 tcp_stamp_us_delta(u64 t1, u64 t0)\n{\n\treturn max_t(s64, t1 - t0, 0);\n}",
        "static inline u32 tcp_stamp_us_delta(u64 t1, u64 t0)\n{\n\treturn max_t(s64, t1 - t0, 0);\n}\n\nstatic inline u32 tcp_stamp32_us_delta(u32 t1, u32 t0)\n{\n\treturn max_t(s32, t1 - t0, 0);\n}",
        "tcp_stamp32_us_delta",
    )
    replace_once(
        "include/net/tcp.h",
        """\t\tstruct {
\t\t\t/* There is space for up to 24 bytes */
\t\t\t__u32 in_flight:30,/* Bytes in flight at transmit */
\t\t\t      is_app_limited:1, /* cwnd not fully used? */
\t\t\t      unused:1;
\t\t\t/* pkts S/ACKed so far upon tx of skb, incl retrans: */
\t\t\t__u32 delivered;
\t\t\t/* start of send pipeline phase */
\t\t\tu64 first_tx_mstamp;
\t\t\t/* when we reached the "delivered" count */
\t\t\tu64 delivered_mstamp;
\t\t} tx;   /* only used for outgoing skbs */""",
        """\t\tstruct {
#define TCPCB_DELIVERED_CE_MASK ((1U << 20) - 1)
#define TCPCB_IN_FLIGHT_BITS 20
#define TCPCB_IN_FLIGHT_MAX ((1U << TCPCB_IN_FLIGHT_BITS) - 1)
\t\t\t/* There is space for up to 24 bytes */
\t\t\t__u32 is_app_limited:1, /* cwnd not fully used? */
\t\t\t      delivered_ce:20,
\t\t\t      unused:11;
\t\t\t/* pkts S/ACKed so far upon tx of skb, incl retrans: */
\t\t\t__u32 delivered;
\t\t\t/* start of send pipeline phase */
\t\t\tu32 first_tx_mstamp;
\t\t\t/* when we reached the "delivered" count */
\t\t\tu32 delivered_mstamp;
\t\t\tu32 in_flight:20,   /* packets in flight at transmit */
\t\t\t    unused2:12;
\t\t\tu32 lost;\t/* packets lost so far upon tx of skb */
\t\t} tx;   /* only used for outgoing skbs */""",
        "tcp_skb_cb.tx 24B layout",
    )
    replace_once(
        "include/net/tcp.h",
        """/* Requires ECN/ECT set on all packets */
#define TCP_CONG_NEEDS_ECN\t0x2
#define TCP_CONG_MASK\t(TCP_CONG_NON_RESTRICTED | TCP_CONG_NEEDS_ECN)""",
        """/* Requires ECN/ECT set on all packets */
#define TCP_CONG_NEEDS_ECN\t0x2
/* Wants notification of CE events (CA_EVENT_ECN_IS_CE, CA_EVENT_ECN_NO_CE). */
#define TCP_CONG_WANTS_CE_EVENTS\t0x4
#define TCP_CONG_MASK\t(TCP_CONG_NON_RESTRICTED | \\
\t\t\t TCP_CONG_NEEDS_ECN | \\
\t\t\t TCP_CONG_WANTS_CE_EVENTS)""",
        "TCP_CONG_WANTS_CE_EVENTS",
    )
    replace_once(
        "include/net/tcp.h",
        """struct rate_sample {
\tu64  prior_mstamp; /* starting timestamp for interval */
\tu32  prior_delivered;\t/* tp->delivered at "prior_mstamp" */
\ts32  delivered;\t\t/* number of packets delivered over interval */
\tlong interval_us;\t/* time for tp->delivered to incr "delivered" */
\tlong rtt_us;\t\t/* RTT of last (S)ACKed packet (or -1) */
\tint  losses;\t\t/* number of packets marked lost upon ACK */
\tu32  acked_sacked;\t/* number of packets newly (S)ACKed upon ACK */
\tu32  prior_in_flight;\t/* in flight before this ACK */
\tbool is_app_limited;\t/* is sample from packet with bubble in pipe? */
\tbool is_retrans;\t/* is sample from retransmission? */
};""",
        """struct rate_sample {
\tu64  prior_mstamp; /* starting timestamp for interval */
\tu32  prior_lost;\t/* tp->lost at "prior_mstamp" */
\tu32  prior_delivered;\t/* tp->delivered at "prior_mstamp" */
\tu32  prior_delivered_ce;/* tp->delivered_ce at "prior_mstamp" */
\tu32  tx_in_flight;\t/* packets in flight at starting timestamp */
\ts32  lost;\t\t/* number of packets lost over interval */
\ts32  delivered;\t\t/* number of packets delivered over interval */
\ts32  delivered_ce;\t/* packets delivered w/ CE mark over interval */
\tlong interval_us;\t/* time for tp->delivered to incr "delivered" */
\tlong rtt_us;\t\t/* RTT of last (S)ACKed packet (or -1) */
\tint  losses;\t\t/* number of packets marked lost upon ACK */
\tu32  acked_sacked;\t/* number of packets newly (S)ACKed upon ACK */
\tu32  prior_in_flight;\t/* in flight before this ACK */
\tbool is_app_limited;\t/* is sample from packet with bubble in pipe? */
\tbool is_retrans;\t/* is sample from retransmission? */
\tbool is_ack_delayed;\t/* is this (likely) a delayed ACK? */
\tbool is_ece;\t\t/* did this ACK have ECN marked? */
};""",
        "struct rate_sample fields",
    )
    replace_once(
        "include/net/tcp.h",
        """\t/* override sysctl_tcp_min_tso_segs */
\tu32 (*min_tso_segs)(struct sock *sk);""",
        """\t/* override sysctl_tcp_min_tso_segs */
\tu32 (*min_tso_segs)(struct sock *sk);
\t/* pick target number of segments per TSO/GSO skb (optional): */
\tu32 (*tso_segs)(struct sock *sk, unsigned int mss_now);
\t/* react to a specific lost skb (optional) */
\tvoid (*skb_marked_lost)(struct sock *sk, const struct sk_buff *skb);""",
        "tcp_congestion_ops tso_segs & skb_marked_lost",
    )
    replace_once(
        "include/net/tcp.h",
        """static inline bool tcp_ca_needs_ecn(const struct sock *sk)
{
\tconst struct inet_connection_sock *icsk = inet_csk(sk);

\treturn icsk->icsk_ca_ops->flags & TCP_CONG_NEEDS_ECN;
}""",
        """static inline bool tcp_ca_wants_ce_events(const struct sock *sk)
{
\tconst struct inet_connection_sock *icsk = inet_csk(sk);

\treturn icsk->icsk_ca_ops->flags & (TCP_CONG_NEEDS_ECN |
\t\t\t\t\t   TCP_CONG_WANTS_CE_EVENTS);
}

static inline bool tcp_ca_needs_ecn(const struct sock *sk)
{
\tconst struct inet_connection_sock *icsk = inet_csk(sk);

\treturn icsk->icsk_ca_ops->flags & TCP_CONG_NEEDS_ECN;
}""",
        "tcp_ca_wants_ce_events",
    )
    replace_once(
        "include/net/tcp.h",
        "/* From tcp_rate.c */\nvoid tcp_rate_skb_sent(struct sock *sk, struct sk_buff *skb);",
        "/* From tcp_rate.c */\nvoid tcp_set_tx_in_flight(struct sock *sk, struct sk_buff *skb);\nvoid tcp_rate_skb_sent(struct sock *sk, struct sk_buff *skb);",
        "tcp_set_tx_in_flight decl",
    )

    # include/uapi/linux/inet_diag.h
    replace_once(
        "include/uapi/linux/inet_diag.h",
        """struct tcp_bbr_info {
\t/* u64 bw: max-filtered BW (app throughput) estimate in Byte per sec: */
\t__u32\tbbr_bw_lo;\t\t/* lower 32 bits of bw */
\t__u32\tbbr_bw_hi;\t\t/* upper 32 bits of bw */
\t__u32\tbbr_min_rtt;\t\t/* min-filtered RTT in uSec */
\t__u32\tbbr_pacing_gain;\t/* pacing gain shifted left 8 bits */
\t__u32\tbbr_cwnd_gain;\t\t/* cwnd gain shifted left 8 bits */
};

union tcp_cc_info {
\tstruct tcpvegas_info\tvegas;
\tstruct tcp_dctcp_info\tdctcp;
\tstruct tcp_bbr_info\tbbr;
};""",
        """struct tcp_bbr_info {
\t/* u64 bw: max-filtered BW (app throughput) estimate in Byte per sec: */
\t__u32\tbbr_bw_lo;\t\t/* lower 32 bits of bw */
\t__u32\tbbr_bw_hi;\t\t/* upper 32 bits of bw */
\t__u32\tbbr_min_rtt;\t\t/* min-filtered RTT in uSec */
\t__u32\tbbr_pacing_gain;\t/* pacing gain shifted left 8 bits */
\t__u32\tbbr_cwnd_gain;\t\t/* cwnd gain shifted left 8 bits */
};

enum tcp_bbr2_phase {
\tBBR2_PHASE_INVALID\t\t= 0,
\tBBR2_PHASE_STARTUP\t\t= 1,
\tBBR2_PHASE_DRAIN\t\t= 2,
\tBBR2_PHASE_PROBE_RTT\t\t= 3,
\tBBR2_PHASE_PROBE_BW_UP\t\t= 4,
\tBBR2_PHASE_PROBE_BW_DOWN\t= 5,
\tBBR2_PHASE_PROBE_BW_CRUISE\t= 6,
\tBBR2_PHASE_PROBE_BW_REFILL\t= 7
};

struct tcp_bbr2_info {
\t__u32\tbbr_bw_lsb;\t\t/* lower 32 bits of bw */
\t__u32\tbbr_bw_msb;\t\t/* upper 32 bits of bw */
\t__u32\tbbr_min_rtt;\t\t/* min-filtered RTT in uSec */
\t__u32\tbbr_pacing_gain;\t/* pacing gain shifted left 8 bits */
\t__u32\tbbr_cwnd_gain;\t\t/* cwnd gain shifted left 8 bits */
\t__u32\tbbr_bw_hi_lsb;\t\t/* lower 32 bits of bw_hi */
\t__u32\tbbr_bw_hi_msb;\t\t/* upper 32 bits of bw_hi */
\t__u32\tbbr_bw_lo_lsb;\t\t/* lower 32 bits of bw_lo */
\t__u32\tbbr_bw_lo_msb;\t\t/* upper 32 bits of bw_lo */
\t__u8\tbbr_mode;\t\t/* current bbr_mode in state machine */
\t__u8\tbbr_phase;\t\t/* current state machine phase */
\t__u8\tunused1;\t\t/* alignment padding; not used yet */
\t__u8\tbbr_version;\t\t/* MUST be at this offset in struct */
\t__u32\tbbr_inflight_lo;\t/* lower/short-term data volume bound */
\t__u32\tbbr_inflight_hi;\t/* higher/long-term data volume bound */
\t__u32\tbbr_extra_acked;\t/* max excess packets ACKed in epoch */
};

union tcp_cc_info {
\tstruct tcpvegas_info\tvegas;
\tstruct tcp_dctcp_info\tdctcp;
\tstruct tcp_bbr_info\tbbr;
\tstruct tcp_bbr2_info\tbbr2;
};""",
        "tcp_bbr2_info diag",
    )

    # net/ipv4/tcp_rate.c
    replace_once(
        "net/ipv4/tcp_rate.c",
        """/* Snapshot the current delivery information in the skb, to generate
 * a rate sample later when the skb is (s)acked in tcp_rate_skb_delivered().
 */
void tcp_rate_skb_sent(struct sock *sk, struct sk_buff *skb)""",
        """void tcp_set_tx_in_flight(struct sock *sk, struct sk_buff *skb)
{
\tstruct tcp_sock *tp = tcp_sk(sk);
\tu32 in_flight;

\t/* Check, sanitize, and record packets in flight after skb was sent. */
\tin_flight = tcp_packets_in_flight(tp) + tcp_skb_pcount(skb);
\tif (WARN_ONCE(in_flight > TCPCB_IN_FLIGHT_MAX,
\t\t      "insane in_flight %u cc %s mss %u "
\t\t      "cwnd %u pif %u %u %u %u\\n",
\t\t      in_flight, inet_csk(sk)->icsk_ca_ops->name,
\t\t      tp->mss_cache, tp->snd_cwnd,
\t\t      tp->packets_out, tp->retrans_out,
\t\t      tp->sacked_out, tp->lost_out))
\t\tin_flight = TCPCB_IN_FLIGHT_MAX;
\tTCP_SKB_CB(skb)->tx.in_flight = in_flight;
}

/* Snapshot the current delivery information in the skb, to generate
 * a rate sample later when the skb is (s)acked in tcp_rate_skb_delivered().
 */
void tcp_rate_skb_sent(struct sock *sk, struct sk_buff *skb)""",
        "tcp_set_tx_in_flight impl",
    )
    replace_once(
        "net/ipv4/tcp_rate.c",
        """\tTCP_SKB_CB(skb)->tx.first_tx_mstamp\t= tp->first_tx_mstamp;
\tTCP_SKB_CB(skb)->tx.delivered_mstamp\t= tp->delivered_mstamp;
\tTCP_SKB_CB(skb)->tx.delivered\t\t= tp->delivered;
\tTCP_SKB_CB(skb)->tx.is_app_limited\t= tp->app_limited ? 1 : 0;""",
        """\tTCP_SKB_CB(skb)->tx.first_tx_mstamp\t= (u32)tp->first_tx_mstamp;
\tTCP_SKB_CB(skb)->tx.delivered_mstamp\t= ((u32)tp->delivered_mstamp) ? : 1;
\tTCP_SKB_CB(skb)->tx.delivered\t\t= tp->delivered;
\tTCP_SKB_CB(skb)->tx.delivered_ce\t= tp->delivered_ce;
\tTCP_SKB_CB(skb)->tx.lost\t\t= tp->lost;
\tTCP_SKB_CB(skb)->tx.is_app_limited\t= tp->app_limited ? 1 : 0;
\ttcp_set_tx_in_flight(sk, skb);""",
        "tcp_rate_skb_sent fields",
    )
    replace_once(
        "net/ipv4/tcp_rate.c",
        """\tif (!rs->prior_delivered ||
\t    after(scb->tx.delivered, rs->prior_delivered)) {
\t\trs->prior_delivered  = scb->tx.delivered;
\t\trs->prior_mstamp     = scb->tx.delivered_mstamp;
\t\trs->is_app_limited   = scb->tx.is_app_limited;
\t\trs->is_retrans\t     = scb->sacked & TCPCB_RETRANS;

\t\t/* Find the duration of the "send phase" of this window: */
\t\trs->interval_us      = tcp_stamp_us_delta(
\t\t\t\t\t\tskb->skb_mstamp,
\t\t\t\t\t\tscb->tx.first_tx_mstamp);""",
        """\tif (!rs->prior_delivered ||
\t    after(scb->tx.delivered, rs->prior_delivered)) {
\t\trs->prior_lost\t     = scb->tx.lost;
\t\trs->prior_delivered_ce  = scb->tx.delivered_ce;
\t\trs->prior_delivered  = scb->tx.delivered;
\t\trs->prior_mstamp     = scb->tx.delivered_mstamp;
\t\trs->is_app_limited   = scb->tx.is_app_limited;
\t\trs->is_retrans\t     = scb->sacked & TCPCB_RETRANS;
\t\trs->tx_in_flight     = scb->tx.in_flight;

\t\t/* Find the duration of the "send phase" of this window: */
\t\trs->interval_us      = tcp_stamp32_us_delta(
\t\t\t\t\t\t(u32)skb->skb_mstamp,
\t\t\t\t\t\tscb->tx.first_tx_mstamp);""",
        "tcp_rate_skb_delivered fields",
    )
    replace_once(
        "net/ipv4/tcp_rate.c",
        """\trs->delivered   = tp->delivered - rs->prior_delivered;

\t/* Model sending data and receiving ACKs as separate pipeline phases
\t * for a window. Usually the ACK phase is longer, but with ACK
\t * compression the send phase can be longer. To be safe we use the
\t * longer phase.
\t */
\tsnd_us = rs->interval_us;\t\t\t\t/* send phase */
\tack_us = tcp_stamp_us_delta(tp->tcp_mstamp,
\t\t\t\t    rs->prior_mstamp); /* ack phase */""",
        """\trs->delivered   = tp->delivered - rs->prior_delivered;
\trs->lost        = tp->lost - rs->prior_lost;
\trs->delivered_ce = tp->delivered_ce - rs->prior_delivered_ce;
\trs->delivered_ce &= TCPCB_DELIVERED_CE_MASK;

\t/* Model sending data and receiving ACKs as separate pipeline phases
\t * for a window. Usually the ACK phase is longer, but with ACK
\t * compression the send phase can be longer. To be safe we use the
\t * longer phase.
\t */
\tsnd_us = rs->interval_us;\t\t\t\t/* send phase */
\tack_us = tcp_stamp32_us_delta((u32)tp->tcp_mstamp,
\t\t\t\t    (u32)rs->prior_mstamp); /* ack phase */""",
        "tcp_rate_gen fields",
    )

    # net/ipv4/tcp_input.c
    replace_once(
        "net/ipv4/tcp_input.c",
        """\tcase INET_ECN_CE:
\t\tif (tcp_ca_needs_ecn(sk))
\t\t\ttcp_ca_event(sk, CA_EVENT_ECN_IS_CE);

\t\tif (!(tp->ecn_flags & TCP_ECN_DEMAND_CWR)) {
\t\t\t/* Better not delay acks, sender can have a very low cwnd */
\t\t\ttcp_enter_quickack_mode(sk, 2);
\t\t\ttp->ecn_flags |= TCP_ECN_DEMAND_CWR;
\t\t}
\t\ttp->ecn_flags |= TCP_ECN_SEEN;
\t\tbreak;
\tdefault:
\t\tif (tcp_ca_needs_ecn(sk))
\t\t\ttcp_ca_event(sk, CA_EVENT_ECN_NO_CE);""",
        """\tcase INET_ECN_CE:
\t\tif (tcp_ca_wants_ce_events(sk))
\t\t\ttcp_ca_event(sk, CA_EVENT_ECN_IS_CE);

\t\tif (!(tp->ecn_flags & TCP_ECN_DEMAND_CWR)) {
\t\t\t/* Better not delay acks, sender can have a very low cwnd */
\t\t\ttcp_enter_quickack_mode(sk, 2);
\t\t\ttp->ecn_flags |= TCP_ECN_DEMAND_CWR;
\t\t}
\t\ttp->ecn_flags |= TCP_ECN_SEEN;
\t\tbreak;
\tdefault:
\t\tif (tcp_ca_wants_ce_events(sk))
\t\t\ttcp_ca_event(sk, CA_EVENT_ECN_NO_CE);""",
        "__tcp_ecn_check_ce CE events",
    )
    replace_once(
        "net/ipv4/tcp_input.c",
        """static void tcp_sum_lost(struct tcp_sock *tp, struct sk_buff *skb)
{
\t__u8 sacked = TCP_SKB_CB(skb)->sacked;

\tif (!(sacked & TCPCB_LOST) ||
\t    ((sacked & TCPCB_LOST) && (sacked & TCPCB_SACKED_RETRANS)))
\t\ttp->lost += tcp_skb_pcount(skb);
}""",
        """static void tcp_sum_lost(struct tcp_sock *tp, struct sk_buff *skb)
{
\t__u8 sacked = TCP_SKB_CB(skb)->sacked;

\tif (!(sacked & TCPCB_LOST) ||
\t    ((sacked & TCPCB_LOST) && (sacked & TCPCB_SACKED_RETRANS))) {
\t\tstruct sock *sk = (struct sock *)tp;
\t\tconst struct tcp_congestion_ops *ca_ops = inet_csk(sk)->icsk_ca_ops;

\t\ttp->lost += tcp_skb_pcount(skb);
\t\tif (ca_ops->skb_marked_lost)
\t\t\tca_ops->skb_marked_lost(sk, skb);
\t}
}""",
        "tcp_sum_lost skb_marked_lost callback",
    )
    replace_once(
        "net/ipv4/tcp_input.c",
        """\ttcp_skb_pcount_add(prev, pcount);
\tWARN_ON_ONCE(tcp_skb_pcount(skb) < pcount);
\ttcp_skb_pcount_add(skb, -pcount);

\t/* When we're adding to gso_segs == 1""",
        """\ttcp_skb_pcount_add(prev, pcount);
\tWARN_ON_ONCE(tcp_skb_pcount(skb) < pcount);
\ttcp_skb_pcount_add(skb, -pcount);

\t/* Adjust tx.in_flight as pcount is shifted from skb to prev. */
\tif (WARN_ONCE(TCP_SKB_CB(skb)->tx.in_flight < pcount,
\t\t      "prev in_flight: %u skb in_flight: %u pcount: %u",
\t\t      TCP_SKB_CB(prev)->tx.in_flight,
\t\t      TCP_SKB_CB(skb)->tx.in_flight,
\t\t      pcount))
\t\tTCP_SKB_CB(skb)->tx.in_flight = 0;
\telse
\t\tTCP_SKB_CB(skb)->tx.in_flight -= pcount;
\tTCP_SKB_CB(prev)->tx.in_flight += pcount;

\t/* When we're adding to gso_segs == 1""",
        "tcp_shifted_skb tx.in_flight",
    )
    replace_once(
        "net/ipv4/tcp_input.c",
        """\tdelivered = tcp_newly_delivered(sk, delivered, flag);
\tlost = tp->lost - lost;\t\t\t/* freshly marked lost */
\ttcp_rate_gen(sk, delivered, lost, is_sack_reneg, sack_state.rate);""",
        """\tdelivered = tcp_newly_delivered(sk, delivered, flag);
\tlost = tp->lost - lost;\t\t\t/* freshly marked lost */
\trs.is_ece = !!(flag & FLAG_ECE);
\ttcp_rate_gen(sk, delivered, lost, is_sack_reneg, sack_state.rate);""",
        "tcp_ack rs.is_ece",
    )
    replace_once(
        "net/ipv4/tcp_input.c",
        """\tif (((tp->rcv_nxt - tp->rcv_wup) > (inet_csk(sk)->icsk_ack.rcv_mss) *
\t\t\t\t\tsysctl_tcp_delack_seg &&
\t     /* ... and right edge of window advances far enough.
\t      * (tcp_recvmsg() will send ACK otherwise). Or...
\t      */
\t     __tcp_select_window(sk) >= tp->rcv_wnd) ||
\t    /* We ACK each frame or... */
\t    tcp_in_quickack_mode(sk) ||
\t    /* We have out of order data. */""",
        """\tif (((tp->rcv_nxt - tp->rcv_wup) > (inet_csk(sk)->icsk_ack.rcv_mss) *
\t\t\t\t\tsysctl_tcp_delack_seg &&
\t     (tp->fast_ack_mode == 1 ||
\t     /* ... and right edge of window advances far enough.
\t      * (tcp_recvmsg() will send ACK otherwise). Or...
\t      */
\t     __tcp_select_window(sk) >= tp->rcv_wnd)) ||
\t    /* We ACK each frame or... */
\t    tcp_in_quickack_mode(sk) ||
\t    /* Protocol state mandates a one-time immediate ACK */
\t    (inet_csk(sk)->icsk_ack.pending & ICSK_ACK_NOW) ||
\t    /* We have out of order data. */""",
        "__tcp_ack_snd_check fast_ack_mode + ICSK_ACK_NOW",
    )

    # net/ipv4/tcp_output.c
    replace_once(
        "net/ipv4/tcp_output.c",
        """\tif (val > tp->tcp_wstamp_ns)
\t\ttp->tcp_wstamp_ns = val;

\tval = div_u64(val, NSEC_PER_USEC);""",
        """\tif (val > tp->tcp_wstamp_ns)
\t\ttp->tcp_wstamp_ns = val;

\ttp->tcp_clock_cache = val;
\tval = div_u64(val, NSEC_PER_USEC);""",
        "tcp_mstamp_refresh tcp_clock_cache",
    )
    replace_once(
        "net/ipv4/tcp_output.c",
        """\t\t} else if (!tcp_ca_needs_ecn(sk)) {
\t\t\t/* ACK or retransmitted segment: clear ECT|CE */""",
        """\t\t} else if (!(tp->ecn_flags & TCP_ECN_ECT_PERMANENT) &&
\t\t\t   !tcp_ca_needs_ecn(sk)) {
\t\t\t/* ACK or retransmitted segment: clear ECT|CE */""",
        "tcp_ecn_send TCP_ECN_ECT_PERMANENT",
    )
    replace_once(
        "net/ipv4/tcp_output.c",
        "\tint nsize, old_factor;\n\tlong limit;",
        "\tint nsize, old_factor, inflight_prev;\n\tlong limit;",
        "tcp_fragment inflight_prev var",
    )
    replace_once(
        "net/ipv4/tcp_output.c",
        """\t\tif (diff)
\t\t\ttcp_adjust_pcount(sk, skb, diff);
\t}

\t/* Link BUFF into the send queue. */""",
        """\t\tif (diff)
\t\t\ttcp_adjust_pcount(sk, skb, diff);

\t\t/* Set buff tx.in_flight as if buff were sent by itself. */
\t\tinflight_prev = TCP_SKB_CB(skb)->tx.in_flight - old_factor;
\t\tif (WARN_ONCE(inflight_prev < 0,
\t\t\t      "inconsistent: tx.in_flight: %u old_factor: %d",
\t\t\t      TCP_SKB_CB(skb)->tx.in_flight, old_factor))
\t\t\tinflight_prev = 0;
\t\tTCP_SKB_CB(buff)->tx.in_flight = inflight_prev +
\t\t\t\t\t\t tcp_skb_pcount(buff);
\t}

\t/* Link BUFF into the send queue. */""",
        "tcp_fragment tx.in_flight",
    )
    replace_once(
        "net/ipv4/tcp_output.c",
        """static u32 tcp_tso_segs(struct sock *sk, unsigned int mss_now)
{
\tconst struct tcp_congestion_ops *ca_ops = inet_csk(sk)->icsk_ca_ops;
\tu32 min_tso, tso_segs;

\tmin_tso = ca_ops->min_tso_segs ?
\t\t\tca_ops->min_tso_segs(sk) :
\t\t\tsysctl_tcp_min_tso_segs;

\ttso_segs = tcp_tso_autosize(sk, mss_now, min_tso);
\treturn min_t(u32, tso_segs, sk->sk_gso_max_segs);
}""",
        """static u32 tcp_tso_segs(struct sock *sk, unsigned int mss_now)
{
\tconst struct tcp_congestion_ops *ca_ops = inet_csk(sk)->icsk_ca_ops;
\tu32 min_tso, tso_segs;

\tif (ca_ops->tso_segs)
\t\treturn min_t(u32, ca_ops->tso_segs(sk, mss_now), sk->sk_gso_max_segs);

\tmin_tso = ca_ops->min_tso_segs ?
\t\t\tca_ops->min_tso_segs(sk) :
\t\t\tsysctl_tcp_min_tso_segs;

\ttso_segs = tcp_tso_autosize(sk, mss_now, min_tso);
\treturn min_t(u32, tso_segs, sk->sk_gso_max_segs);
}""",
        "tcp_tso_segs ca_ops->tso_segs",
    )
    replace_once(
        "net/ipv4/tcp_output.c",
        """\t\t\tskb->skb_mstamp = tp->tcp_mstamp;
\t\t\tgoto repair; /* Skip network transmission */""",
        """\t\t\tskb->skb_mstamp = tp->tcp_mstamp;
\t\t\ttcp_set_tx_in_flight(sk, skb);
\t\t\tgoto repair; /* Skip network transmission */""",
        "tcp_write_xmit repair tx_in_flight",
    )

    # net/ipv4/tcp.c & tcp_cong.c fast_ack_mode reset
    replace_once(
        "net/ipv4/tcp.c",
        "\ttp->rx_opt.dsack = 0;\n\ttp->rx_opt.num_sacks = 0;",
        "\ttp->rx_opt.dsack = 0;\n\ttp->rx_opt.num_sacks = 0;\n\ttp->fast_ack_mode = 0;",
        "tcp_disconnect reset fast_ack_mode",
    )
    replace_once(
        "net/ipv4/tcp_cong.c",
        "\ttcp_sk(sk)->prior_ssthresh = 0;\n\tif (icsk->icsk_ca_ops->init)",
        "\ttcp_sk(sk)->prior_ssthresh = 0;\n\ttcp_sk(sk)->fast_ack_mode = 0;\n\tif (icsk->icsk_ca_ops->init)",
        "tcp_init_congestion_control reset fast_ack_mode",
    )

    # net/ipv4/Kconfig & Makefile for BBR2
    replace_once(
        "net/ipv4/Kconfig",
        """\tsignal. It requires the fq ("Fair Queue") pacing packet scheduler.

choice
\tprompt "Default TCP congestion control\"""",
        """\tsignal. It requires the fq ("Fair Queue") pacing packet scheduler.

config TCP_CONG_BBR2
\ttristate "BBR2 TCP"
\tdefault n
\t---help---
\t  BBRv2 congestion control algorithm from Google Linux 5.13.

choice
\tprompt "Default TCP congestion control\"""",
        "net/ipv4/Kconfig TCP_CONG_BBR2",
    )
    replace_once(
        "net/ipv4/Kconfig",
        """\tconfig DEFAULT_BBR
\t\tbool "BBR" if TCP_CONG_BBR=y

\tconfig DEFAULT_RENO""",
        """\tconfig DEFAULT_BBR
\t\tbool "BBR" if TCP_CONG_BBR=y

\tconfig DEFAULT_BBR2
\t\tbool "BBR2" if TCP_CONG_BBR2=y

\tconfig DEFAULT_RENO""",
        "net/ipv4/Kconfig DEFAULT_BBR2",
    )
    replace_once(
        "net/ipv4/Kconfig",
        """\tdefault "bbr" if DEFAULT_BBR
\tdefault "cubic\"""",
        """\tdefault "bbr" if DEFAULT_BBR
\tdefault "bbr2" if DEFAULT_BBR2
\tdefault "cubic\"""",
        "net/ipv4/Kconfig DEFAULT_TCP_CONG bbr2",
    )
    replace_once(
        "net/ipv4/Makefile",
        "obj-$(CONFIG_TCP_CONG_BBR) += tcp_bbr.o",
        "obj-$(CONFIG_TCP_CONG_BBR) += tcp_bbr.o\nobj-$(CONFIG_TCP_CONG_BBR2) += tcp_bbr2.o",
        "net/ipv4/Makefile tcp_bbr2.o",
    )

    print("=== [2/4] Backporting sch_cake (4.19/5.x AQM) ===")
    shutil.copyfile(os.path.join(bdir, "sch_cake.c"), os.path.join(kdir, "net/sched/sch_cake.c"))
    shutil.copyfile(os.path.join(bdir, "cobalt_compat.h"), os.path.join(kdir, "net/sched/cobalt_compat.h"))

    cake_uapi = """\t__u32 ecn_mark;         /* packets marked with ecn*/
};

/* CAKE */
enum {
\tTCA_CAKE_UNSPEC,
\tTCA_CAKE_PAD,
\tTCA_CAKE_BASE_RATE64,
\tTCA_CAKE_DIFFSERV_MODE,
\tTCA_CAKE_ATM,
\tTCA_CAKE_FLOW_MODE,
\tTCA_CAKE_OVERHEAD,
\tTCA_CAKE_RTT,
\tTCA_CAKE_TARGET,
\tTCA_CAKE_AUTORATE,
\tTCA_CAKE_MEMORY,
\tTCA_CAKE_NAT,
\tTCA_CAKE_RAW,
\tTCA_CAKE_WASH,
\tTCA_CAKE_MPU,
\tTCA_CAKE_INGRESS,
\tTCA_CAKE_ACK_FILTER,
\tTCA_CAKE_SPLIT_GSO,
\tTCA_CAKE_FWMARK,
\t__TCA_CAKE_MAX
};
#define TCA_CAKE_MAX\t(__TCA_CAKE_MAX - 1)

enum {
\t__TCA_CAKE_STATS_INVALID,
\tTCA_CAKE_STATS_PAD,
\tTCA_CAKE_STATS_CAPACITY_ESTIMATE64,
\tTCA_CAKE_STATS_MEMORY_LIMIT,
\tTCA_CAKE_STATS_MEMORY_USED,
\tTCA_CAKE_STATS_AVG_NETOFF,
\tTCA_CAKE_STATS_MIN_NETLEN,
\tTCA_CAKE_STATS_MAX_NETLEN,
\tTCA_CAKE_STATS_MIN_ADJLEN,
\tTCA_CAKE_STATS_MAX_ADJLEN,
\tTCA_CAKE_STATS_TIN_STATS,
\tTCA_CAKE_STATS_DEFICIT,
\tTCA_CAKE_STATS_COBALT_COUNT,
\tTCA_CAKE_STATS_DROPPING,
\tTCA_CAKE_STATS_DROP_NEXT_US,
\tTCA_CAKE_STATS_P_DROP,
\tTCA_CAKE_STATS_BLUE_TIMER_US,
\t__TCA_CAKE_STATS_MAX
};
#define TCA_CAKE_STATS_MAX (__TCA_CAKE_STATS_MAX - 1)

enum {
\t__TCA_CAKE_TIN_STATS_INVALID,
\tTCA_CAKE_TIN_STATS_PAD,
\tTCA_CAKE_TIN_STATS_SENT_PACKETS,
\tTCA_CAKE_TIN_STATS_SENT_BYTES64,
\tTCA_CAKE_TIN_STATS_DROPPED_PACKETS,
\tTCA_CAKE_TIN_STATS_DROPPED_BYTES64,
\tTCA_CAKE_TIN_STATS_ACKS_DROPPED_PACKETS,
\tTCA_CAKE_TIN_STATS_ACKS_DROPPED_BYTES64,
\tTCA_CAKE_TIN_STATS_ECN_MARKED_PACKETS,
\tTCA_CAKE_TIN_STATS_ECN_MARKED_BYTES64,
\tTCA_CAKE_TIN_STATS_BACKLOG_PACKETS,
\tTCA_CAKE_TIN_STATS_BACKLOG_BYTES,
\tTCA_CAKE_TIN_STATS_THRESHOLD_RATE64,
\tTCA_CAKE_TIN_STATS_TARGET_US,
\tTCA_CAKE_TIN_STATS_INTERVAL_US,
\tTCA_CAKE_TIN_STATS_WAY_INDIRECT_HITS,
\tTCA_CAKE_TIN_STATS_WAY_MISSES,
\tTCA_CAKE_TIN_STATS_WAY_COLLISIONS,
\tTCA_CAKE_TIN_STATS_PEAK_DELAY_US,
\tTCA_CAKE_TIN_STATS_AVG_DELAY_US,
\tTCA_CAKE_TIN_STATS_BASE_DELAY_US,
\tTCA_CAKE_TIN_STATS_SPARSE_FLOWS,
\tTCA_CAKE_TIN_STATS_BULK_FLOWS,
\tTCA_CAKE_TIN_STATS_UNRESPONSIVE_FLOWS,
\tTCA_CAKE_TIN_STATS_MAX_SKBLEN,
\tTCA_CAKE_TIN_STATS_FLOW_QUANTUM,
\t__TCA_CAKE_TIN_STATS_MAX
};
#define TCA_CAKE_TIN_STATS_MAX (__TCA_CAKE_TIN_STATS_MAX - 1)
#define TC_CAKE_MAX_TINS (8)

enum {
\tCAKE_FLOW_NONE = 0,
\tCAKE_FLOW_SRC_IP,
\tCAKE_FLOW_DST_IP,
\tCAKE_FLOW_HOSTS,
\tCAKE_FLOW_FLOWS,
\tCAKE_FLOW_DUAL_SRC,
\tCAKE_FLOW_DUAL_DST,
\tCAKE_FLOW_TRIPLE,
\tCAKE_FLOW_MAX,
};

enum {
\tCAKE_DIFFSERV_DIFFSERV3 = 0,
\tCAKE_DIFFSERV_DIFFSERV4,
\tCAKE_DIFFSERV_DIFFSERV8,
\tCAKE_DIFFSERV_BESTEFFORT,
\tCAKE_DIFFSERV_PRECEDENCE,
\tCAKE_DIFFSERV_MAX
};

enum {
\tCAKE_ACK_NONE = 0,
\tCAKE_ACK_FILTER,
\tCAKE_ACK_AGGRESSIVE,
\tCAKE_ACK_MAX
};

enum {
\tCAKE_ATM_NONE = 0,
\tCAKE_ATM_ATM,
\tCAKE_ATM_PTM,
\tCAKE_ATM_MAX
};
#endif"""

    replace_once(
        "include/uapi/linux/pkt_sched.h",
        "\t__u32 ecn_mark;         /* packets marked with ecn*/\n};\n#endif",
        cake_uapi,
        "include/uapi/linux/pkt_sched.h CAKE enums",
    )
    replace_once(
        "net/sched/Kconfig",
        "config NET_SCH_FQ\n",
        """config NET_SCH_CAKE
\ttristate "Common Applications Kept Enhanced (CAKE)"
\t---help---
\t  Say Y here if you want to use the Common Applications Kept Enhanced
\t  (CAKE) queue management algorithm.

config NET_SCH_FQ
""",
        "net/sched/Kconfig NET_SCH_CAKE",
    )
    replace_once(
        "net/sched/Makefile",
        "obj-$(CONFIG_NET_SCH_FQ)\t+= sch_fq.o",
        "obj-$(CONFIG_NET_SCH_FQ)\t+= sch_fq.o\nobj-$(CONFIG_NET_SCH_CAKE)\t+= sch_cake.o",
        "net/sched/Makefile sch_cake.o",
    )

    print("=== [3/4] Fixing BFQ Multi-Queue Choice in block/Kconfig.iosched ===")
    replace_once(
        "block/Kconfig.iosched",
        """\tconfig DEFAULT_MQ_KYBER
\t\tbool "Kyber" if MQ_IOSCHED_KYBER=y

endchoice

config DEFAULT_MQ_IOSCHED
\tstring
\tdefault "mq-deadline" if DEFAULT_MQ_DEADLINE
\tdefault "kyber" if DEFAULT_MQ_KYBER""",
        """\tconfig DEFAULT_MQ_KYBER
\t\tbool "Kyber" if MQ_IOSCHED_KYBER=y

\tconfig DEFAULT_MQ_BFQ
\t\tbool "BFQ" if IOSCHED_BFQ=y

endchoice

config DEFAULT_MQ_IOSCHED
\tstring
\tdefault "mq-deadline" if DEFAULT_MQ_DEADLINE
\tdefault "kyber" if DEFAULT_MQ_KYBER
\tdefault "bfq" if DEFAULT_MQ_BFQ""",
        "block/Kconfig.iosched DEFAULT_MQ_BFQ",
    )

    print("=== [4/4] Baking Max Internet TCP/Socket/NAPI Tunings into C Defaults ===")
    replace_once(
        "net/ipv4/tcp_output.c",
        "int sysctl_tcp_slow_start_after_idle __read_mostly = 1;",
        "int sysctl_tcp_slow_start_after_idle __read_mostly = 0;",
        "tcp_slow_start_after_idle=0",
    )
    replace_once(
        "net/ipv4/tcp_ipv4.c",
        """\tnet->ipv4.sysctl_tcp_ecn = 1;
\tnet->ipv4.sysctl_tcp_ecn_fallback = 1;""",
        """\tnet->ipv4.sysctl_tcp_ecn = 1;
\tnet->ipv4.sysctl_tcp_ecn_fallback = 1;
\tnet->ipv4.sysctl_tcp_mtu_probing = 1;""",
        "tcp_mtu_probing=1",
    )
    replace_once(
        "net/ipv4/tcp_ipv4.c",
        "\tnet->ipv4.sysctl_tcp_fin_timeout = TCP_FIN_TIMEOUT;",
        "\tnet->ipv4.sysctl_tcp_fin_timeout = 15 * HZ;",
        "tcp_fin_timeout=15s",
    )
    replace_once(
        "net/ipv4/tcp_ipv4.c",
        "\tnet->ipv4.sysctl_tcp_notsent_lowat = UINT_MAX;\n\tnet->ipv4.sysctl_tcp_tw_reuse = 0;",
        "\tnet->ipv4.sysctl_tcp_notsent_lowat = 131072;\n\tnet->ipv4.sysctl_tcp_tw_reuse = 1;",
        "tcp_notsent_lowat=131072 + tw_reuse=1",
    )
    replace_once(
        "net/ipv4/tcp_ipv4.c",
        "\tnet->ipv4.sysctl_tcp_default_init_rwnd = TCP_INIT_CWND * 2;",
        "\tnet->ipv4.sysctl_tcp_default_init_rwnd = 60;",
        "tcp_default_init_rwnd=60",
    )
    replace_once(
        "net/ipv4/tcp_ipv4.c",
        "\tnet->ipv4.sysctl_tcp_fastopen = TFO_CLIENT_ENABLE;\n\tspin_lock_init(&net->ipv4.tcp_fastopen_ctx_lock);\n\tnet->ipv4.sysctl_tcp_fastopen_blackhole_timeout = 60 * 60;",
        "\tnet->ipv4.sysctl_tcp_fastopen = TFO_CLIENT_ENABLE | TFO_SERVER_ENABLE;\n\tspin_lock_init(&net->ipv4.tcp_fastopen_ctx_lock);\n\tnet->ipv4.sysctl_tcp_fastopen_blackhole_timeout = 5 * 60;",
        "tcp_fastopen=3 + blackhole_timeout=300",
    )
    replace_once(
        "net/core/sock.c",
        "__u32 sysctl_wmem_max __read_mostly = SK_WMEM_MAX;\nEXPORT_SYMBOL(sysctl_wmem_max);\n__u32 sysctl_rmem_max __read_mostly = SK_RMEM_MAX;",
        "__u32 sysctl_wmem_max __read_mostly = 4194304;\nEXPORT_SYMBOL(sysctl_wmem_max);\n__u32 sysctl_rmem_max __read_mostly = 4194304;",
        "rmem_max=4MB + wmem_max=4MB",
    )
    replace_once(
        "net/ipv4/tcp.c",
        """\tmax_wshare = min(16UL*1024*1024, limit);
\tmax_rshare = min(16UL*1024*1024, limit);

\tsysctl_tcp_wmem[0] = SK_MEM_QUANTUM;
\tsysctl_tcp_wmem[1] = 16*1024;
\tsysctl_tcp_wmem[2] = max(64*1024, max_wshare);

\tsysctl_tcp_rmem[0] = SK_MEM_QUANTUM;
\tsysctl_tcp_rmem[1] = 87380;
\tsysctl_tcp_rmem[2] = max(87380, max_rshare);""",
        """\tmax_wshare = min(4UL*1024*1024, limit);
\tmax_rshare = min(6UL*1024*1024, limit);

\tsysctl_tcp_wmem[0] = SK_MEM_QUANTUM;
\tsysctl_tcp_wmem[1] = 65536;
\tsysctl_tcp_wmem[2] = max(65536, max_wshare);

\tsysctl_tcp_rmem[0] = SK_MEM_QUANTUM;
\tsysctl_tcp_rmem[1] = 131072;
\tsysctl_tcp_rmem[2] = max(131072, max_rshare);""",
        "tcp_wmem + tcp_rmem tuning",
    )
    replace_once(
        "net/core/dev.c",
        """int netdev_max_backlog __read_mostly = 1000;
EXPORT_SYMBOL(netdev_max_backlog);

int netdev_tstamp_prequeue __read_mostly = 1;
int netdev_budget __read_mostly = 300;
/* Must be at least 2 jiffes to guarantee 1 jiffy timeout */
unsigned int __read_mostly netdev_budget_usecs = 2 * USEC_PER_SEC / HZ;""",
        """int netdev_max_backlog __read_mostly = 2500;
EXPORT_SYMBOL(netdev_max_backlog);

int netdev_tstamp_prequeue __read_mostly = 1;
int netdev_budget __read_mostly = 600;
/* Must be at least 2 jiffes to guarantee 1 jiffy timeout */
unsigned int __read_mostly netdev_budget_usecs = 4000;""",
        "netdev_max_backlog=2500 + netdev_budget=600",
    )

    print("ALL Zareth R5 5.x Backports & Network Tunings Applied Successfully!")


if __name__ == "__main__":
    main()
