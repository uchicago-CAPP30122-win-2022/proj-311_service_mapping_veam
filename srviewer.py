import argparse
from cdp_sr import DataPortalCollector

def main():
    collector = DataPortalCollector()
    limit = 200
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', action="store", type=int, help='the limit of the number of service requests to receive')
    parser.add_argument('--des', action='store_true', help='Sort the service requests by sr_type in Z to A order (default: ascending order)')
  
    args = parser.parse_args()
    
    if args.limit: 
        limit = args.limit
    
    serv_reqs = collector.extract_sr(limit)

    if args.des:
        serv_reqs.sort(reverse=True, key=lambda obj: obj.sr_type)
    else:
        serv_reqs.sort(key=lambda obj: obj.sr_type)

    for serv_req in serv_reqs:
        print(serv_req)
        print("----")


if __name__ == '__main__':
    main() 