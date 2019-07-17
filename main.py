import ip_pool

#自动存，手动更新，也可以自动更新，
ip_pool = ip_pool.IP_POOL()

data = ip_pool.get_ips_from_web()
data = ip_pool.check_ip_port(data)

ip_pool.save_db(data)