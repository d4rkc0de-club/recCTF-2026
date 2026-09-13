This is the first of its series (1/3).

OSINT will be a bit different this time ; Do you need to map out the entirity of the game to solve these challenges? no.

Try solving these ; The slickest/most unexpected writeups get an honorary Red Bull!

Whats the name of the "road" I am on?

flag format: d4rk{name_of_road}

(only 2 tries for this)

answer : d4rk{senora_freeway}

making these levels

```bash
base_url="panorma url" 
files=(
  "0_0.jpg" "0_1.jpg" "0_2.jpg" "0_3.jpg"
  "1_0.jpg" "1_1.jpg" "1_2.jpg" "1_3.jpg"
  "2_0.jpg" "2_1.jpg" "2_2.jpg" "2_3.jpg"
  "3_0.jpg" "3_1.jpg" "3_2.jpg" "3_3.jpg"
  "4_0.jpg" "4_1.jpg" "4_2.jpg" "4_3.jpg"
  "5_0.jpg" "5_1.jpg" "5_2.jpg" "5_3.jpg"
  "6_0.jpg" "6_1.jpg" "6_2.jpg" "6_3.jpg"
  "7_0.jpg" "7_1.jpg" "7_2.jpg" "7_3.jpg"
  "base.jpg"
)

for file in "${files[@]}"; do
  curl -O "${base_url}/${file}"
done
```

```bash
magick \
  \( 0_0.jpg 1_0.jpg 2_0.jpg 3_0.jpg 4_0.jpg 5_0.jpg 6_0.jpg 7_0.jpg +append \) \
  \( 0_1.jpg 1_1.jpg 2_1.jpg 3_1.jpg 4_1.jpg 5_1.jpg 6_1.jpg 7_1.jpg +append \) \
  \( 0_2.jpg 1_2.jpg 2_2.jpg 3_2.jpg 4_2.jpg 5_2.jpg 6_2.jpg 7_2.jpg +append \) \
  \( 0_3.jpg 1_3.jpg 2_3.jpg 3_3.jpg 4_3.jpg 5_3.jpg 6_3.jpg 7_3.jpg +append \) \
  -append stitched.jpg
```
