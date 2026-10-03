title : SAGE's archives

description : the s4g3 archive is a mess. five photographs. no context. no useful captions. every post is from a different point in history. identify each one and connect the answers. 

flag format : d4rk{EventNameInPost1_PersonAndPhotographerWhoTookThePhotoInPost2_OrganizationNameInPost3_CityNameInPost4_ShipNameInPost5}


flag : d4rk{BambathaRebellion_MadameZoéDebeincheAlphonseBertillon_KabushikiGaishaKongōGumi_Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch_SSGreatEastern}

```bash
docker build -t sage-r4ge .
```

```bash
docker run -d \
  --name sage-r4ge \
  -p 127.0.0.1:3011:80 \
  sage-r4ge

```