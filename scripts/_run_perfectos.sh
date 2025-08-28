script=$1
arglist=$2

parallel -j 100 --colsep=' ' -a $arglist python $script {1} {2} {3} {4} {5} {6}
