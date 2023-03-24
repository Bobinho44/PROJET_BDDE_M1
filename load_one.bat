del data/%2.bad
del data/%2.log
sqlldr %1 BAD=data/%2.bad CONTROL=data/%2.ctl LOG=data/%2.log skip=1