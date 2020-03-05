# TCP Original (RFC 793)
if {$argc == 2} {
    set karn   [lindex $argv 0] 
    set jacobson       [lindex $argv 1] 
} else {
    puts "      CBR0-UDP n0"
    puts "                \\"
    puts "                 n2 ---- n3"
    puts "                /"
    puts "      CBR1-TCP n1 "
    puts ""
    puts "  Usage: ns $argv0 karn (true|false) jacobson (true|false)"
    puts ""
    exit 1
}

# Createing the simulator object
set ns [new Simulator]

#file to store results
#
set fname "ex2-trace" 
set nf [open $fname.tr w]
$ns trace-all $nf
set nff [open $fname.rtt w]

#Finishing procedure
proc finish {} {
        global ns nf nff
        $ns flush-trace
        close $nf
        close $nff
        exit 0
}

proc recordTCPTimes { } {
	
	global ns tcp_agents nff cbr_i
	
	set now [$ns now]
	
    for { set index 0 }  { $index < [array size tcp_agents] }  { incr index } {
        writeAgent $tcp_agents($index) $index $nff $now
    }

	$ns at [expr $now+0.1] "recordTCPTimes"
}

proc writeAgent { tcp n nff now args } {
    set rtt  [expr [$tcp set rtt_]  * [$tcp set tcpTick_]]
    set srtt  [expr ([$tcp set srtt_] >> [$tcp set T_SRTT_BITS]) * [$tcp set tcpTick_]]
    set rttvar  [expr ([$tcp set rttvar_] >> [$tcp set T_RTTVAR_BITS]) * [$tcp set tcpTick_]]
    set bo [expr [$tcp set backoff_]]
    set cw  [expr [$tcp set cwnd_]]
    set cwmax  [expr [$tcp set maxcwnd_]]
	puts $nff "$n $now $rtt $srtt $cw $cwmax [expr 0.5*($bo-1)]"
}

#Create 4 nodes
#
#  	     n2
#  	      |
#   	      |
#    n1-------n3--------n4
#   	      |
#  	      |
# 	      n0
 
set n(0) [$ns node]
set n(1) [$ns node]
set n(2) [$ns node]
set n(3) [$ns node]
set n(4) [$ns node]

set tcp_agents(0) [new Agent/TCP]
set tcp_agents(1) [new Agent/TCP/Reno]
set tcp_agents(2) [new Agent/TCP/Vegas]

set cbr_i(0) [new Application/Traffic/CBR]
set cbr_i(1) [new Application/Traffic/CBR]
set cbr_i(2) [new Application/Traffic/CBR]

#Duplex lines between nodes
$ns duplex-link $n(0) $n(3) 5Mb 20ms DropTail
$ns duplex-link $n(1) $n(3) 5Mb 20ms DropTail
$ns duplex-link $n(2) $n(3) 5Mb 20ms DropTail
$ns duplex-link $n(3) $n(4) 1Mb 50ms DropTail

# Node 0: CBR0 TCP0 Tahoe
for { set index 0 }  { $index < [array size tcp_agents] }  { incr index } {
   puts "Setting up tcp agent $index"
   $ns attach-agent $n($index) $tcp_agents($index)
   $cbr_i($index) set rate_ 0.5Mbps
   $cbr_i($index) attach-agent $tcp_agents($index)
   $tcp_agents($index) set class_ $index
   $tcp_agents($index) set tcpTick_ 0.01
   $tcp_agents($index) set add793slowstart_ true
   $tcp_agents($index) set window_ 40
}
pene
# Node 3: No settings
$ns queue-limit $n(0) $n(3) 20
$ns queue-limit $n(1) $n(3) 20
$ns queue-limit $n(2) $n(3) 20

# Node 4: 3 Sinks, one for each tcp agent
# Connect TCP to sinks
for { set index 0 }  { $index < [array size tcp_agents] }  { incr index } {
    set null($index) [new Agent/TCPSink]
    $ns attach-agent $n(4) $null($index)
    $ns connect $tcp_agents($index) $null($index)
    $tcp_agents($index) attach-trace $nff
}
pene
for { set index 0 }  { $index < 20 }  { incr index 2 } {
    set end [expr {$index + 1}]
    $ns at $index "$cbr_i(1) start"
    $ns at $end "$cbr_i(1) stop"
    puts "Starting n1 at $index and stopping it at $end"
}

for { set index 0 }  { $index < 20 }  { incr index } {
    set end [expr {$index + 0.5}]
    $ns at $index "$cbr_i(0) start"
    $ns at $end "$cbr_i(0) stop"
    puts "Starting n0 at $index and stopping it at $end"
}

for { set index 0 }  { $index < 20 }  { incr index 4 } {
    set end [expr {$index + 2}]
    $ns at $index "$cbr_i(2) start"
    $ns at $end "$cbr_i(2) stop"
    puts "Starting n2 at $index and stopping it at $end"
}


$ns at 0.0 "recordTCPTimes"
$ns at 20.0 "finish"

$ns run
pene