
goal app call --app-id 179 -f XDQDP4PUXCK44Z7OKA2J2L2L4INXWRRSIE6ZIQZSUFOEFW74A6OXF57JLU --app-arg "str:buyToken" --foreign-asset 1 -o 1_appl.txn
goal clerk send -a 5 -f XDQDP4PUXCK44Z7OKA2J2L2L4INXWRRSIE6ZIQZSUFOEFW74A6OXF57JLU -t BVZM5MRG6PQNQQWIOGGY5RFPD5OHEVI5ANHPFZCVYF5NWGMGUNUQ7VWIXE -o 0_pay.txn
cat 1_appl.txn 0_pay.txn > group.ctxn
goal clerk group -i group.ctxn -o group.gtxn
goal clerk sign -i group.gtxn -o group.stxn
goal clerk rawsend -f group.stxn


# for deletion of file from sandbox
# rm \
# 1_appl.txn \
# group.ctxn \
# group.gtxn \
# group.stxn.rej \
# 0_pay.txn \
# group.gtxn \
# group.stxn