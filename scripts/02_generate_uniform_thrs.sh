set -e
files=`ls pwms/*.pwm`
for input in $files
do
	output=`echo $input | sed -e 's/pwm$/thr/g' | sed -e 's/pwms/thrs/'`
	echo $input
	echo $output
	java -cp scripts/ape.jar ru.autosome.ape.di.PrecalculateThresholds $input --single-motif --from-mono --discretization 10000 > $output

done
