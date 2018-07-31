#py各种小工具
import builtwith
import whois

# 识别网站所用技术
print(builtwith.parse("https://www.becat.shop"))

# 寻找网站所有者
print(whois.whois("https://www.becat.shop"))