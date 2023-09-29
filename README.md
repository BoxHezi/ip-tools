# ip-tools

## TODO

- [x] cidr to ip function
- [ ] ip and asn query function, ref: https://ipapi.is/developers.html
  - [x] single IP or ASN / multiple IPs or ASNs
  - [ ] Add support for CIDR
- [x] ip lookups, for open ports and vulnerabilities, ref: https://internetdb.shodan.io/
  - [x] single IP or multiple IPs
  - [x] Add support for CIDR
- [ ] result to json, database, etc
  - [x] git repo info to database
    - [x] store hash into database to detect change
  - [ ] cidr to ip info to database
    - [x] store cidr ip mapping in database
    - [ ] check changed ip addresses
      - partially done, now it is able to detect CIDR change for countries
      - Need to check changed IP addresses
- [ ] Add GIT Large File Support for database?
