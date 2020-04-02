# covid-19
This code is an attempt to predict the peak mortality, and the decline of the covid-19 virus.
A similar methodology to that used in the article [Hell is Coming](https://www.insidermonkey.com/blog/hell-is-coming-here-is-the-mathematical-proof-822824/)
is used in this analysis. While the article only talks about peaks, this analysis looks at both the rise and fall of morality.

### Assumptions
There is a lot of information about this virus in articles on the Internet. Some of this information is
conflicting, so I try to focus on facts that are strongly believed to be accurate. Below are the assumptions I've used:
* Mortality is 100% accurate, while confirmed cases are inaccurate because confirming cases requires testing.
* [WHO](https://www.who.int/docs/default-source/coronaviruse/who-china-joint-mission-on-covid-19-final-report.pdf) 
report states it takes 2 to 8 weeks to die from covid-19. [The Lancet report](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30257-7/fulltext)
states that the mean duration from symptom onset to death is 17.8 days (16.9 to 19.2 95% credible interval). The "Hell is Coming"
report used 23 - 24 days, and had a fairly accurate prediction of 800 deaths in the US on March 26th; it was actually 1,275. Given all
of this conflicting information, I used **18 days**.
* Given China implemented a "shelter-in-place" order to its citizens, and that appears to have slowed the mortality rate
I've used the dates for each state's shelter-in-place from the NYTs article "[See Which States and Cities Have Told Residents to Stay at Home](https://www.nytimes.com/interactive/2020/us/coronavirus-stay-at-home-order.html)".
When there were multiple dates for a state, I've used the latest date. Also, as noted in the NYTs article "[Restrictions Are Slowing Coronavirus Infections, New Data Suggest](https://www.nytimes.com/2020/03/30/health/coronavirus-restrictions-fevers.html)"
there is a big different between orders, "closing restaurants and bars and asking people to stay in their homes produced dramatic results in all three cities."
