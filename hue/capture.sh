# We use dnsmasq to provide an IP and make it do less work when
# polling for the internet.
echo "starting dnsmasq"
sudo pkill -9 dnsmasq
sudo timeout 30 dnsmasq -C dnsmasq_config
echo "clearing postrouting table and blocking outgoing acks"
sudo iptables -t mangle -F OUTPUT
sudo iptables -t mangle -A OUTPUT -o eth4 -p tcp --tcp-flags ALL ACK -j DROP

echo "Setting cpu 0 and 1 to performance governor. Enabling low latency mode."
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
sudo sh -c "echo 1 > /proc/sys/net/ipv4/tcp_low_latency"

# don't split, don't parse
#sudo tcpdump -i eth4 -j adapter --time-stamp-precision=nanoseconds -w "data/out.pcap" 

# parse after splitting
#sudo tcpdump -i eth4 -j adapter --time-stamp-precision=nanoseconds -G 30 -w "data/%Y-%m-%d-%H-%M-%S.pcap" -z `pwd`/parse_pcap.py

# split but don't parse
sudo tcpdump -i eth4 -j adapter --time-stamp-precision=nanoseconds -G 15 -w `pwd`/"tmp/%Y-%m-%d-%H-%M-%S.pcap" -z `pwd`/mv.sh

# this will occasionally produce "cannot stat blah" errors. This is
# ok, we run a clean when we switch guesses and don't want the old
# data contaminating the new.
