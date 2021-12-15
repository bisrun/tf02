n = 1260

coin_unit = [500,100,50,10]
coin_count = 0

for i, x in enumerate(coin_unit) :
    (nx, cx) = (n // coin_unit[i], n%coin_unit[i])
    n = cx ;
    coin_count += nx ;

print(coin_count)