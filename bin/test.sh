set -e

cd "$BENCH_ROOT"/BFS  && echo BFS  && ./bfs
cd "$BENCH_ROOT"/BS   && echo BS   && ./bs
cd "$BENCH_ROOT"/CEDD && echo CEDD && ./cedd
cd "$BENCH_ROOT"/CEDT && echo CEDT && ./cedt
cd "$BENCH_ROOT"/HSTI && echo HSTI && ./hsti
cd "$BENCH_ROOT"/HSTO && echo HSTO && ./hsto
cd "$BENCH_ROOT"/PAD  && echo PAD  && ./pad
cd "$BENCH_ROOT"/RSCD && echo RSCD && ./rscd
cd "$BENCH_ROOT"/RSCT && echo RSCT && ./rsct
cd "$BENCH_ROOT"/SC   && echo SC   && ./sc
cd "$BENCH_ROOT"/SSSP && echo SSSP && ./sssp
cd "$BENCH_ROOT"/TQ   && echo TQ   && ./tq
cd "$BENCH_ROOT"/TQH  && echo TQH  && ./tqh
cd "$BENCH_ROOT"/TRNS && echo TRNS && ./trns
