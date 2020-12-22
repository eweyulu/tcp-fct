#! /usr/bin/perl

$timeint = 0.001;
if (defined($opt_t)) {
    $timeint = $opt_t;
}

$_ = <>;
($time, $data) = split;
$sum = 1;
$agg = $data;

$timestart = int($time / $timeint) * $timeint;
$timenext = $timestart + $timeint;

while (<>) {
    ($time, $data) = split;
    while ($time > $timenext) {
        $timeprev = $timenext - $timeint;
        print "$timeprev $sum $agg\n";
        $timenext += $timeint;
        # print "    erhoehe timenext: $timenext\n";
        $sum = 0;
	$agg = 0;
    }
    $sum++;
    $agg += $data; 
    # print "next $time $sum  $timenext\n";
}
# print "$timeprev $sum $agg\n";
$timeprev = $timenext - $timeint;
