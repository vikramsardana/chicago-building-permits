I built an engine (use pandasProgram.py) that lets users enter the balance type (unpaid balance, paid balance, or waived balance), and whether the balance is positive, negative, or zero (yes, surprisingly there were people with, for example, a negative unpaid balance - perhaps they accidentally overpaid their permit fees, or there was some sort of tax credit or other government rebate). They could then enter a desired permit type, and would receive the Bayesian probability of a permit with that unpaid balance being of that permit type.

There is also an option to print out the permit type frequencies for a particular balance, or for all balances. I would have liked to build a UI for this, but unfortunately did not have time.

Using this, we can see that the most permits were given for “Electric Wiring”, which perhaps makes sense as it’s a common building operation. The next most common were for “Easy Permit Process” and “Renovation/Alteration”, then a big dropoff before our next one “Signs”. Interestingly, there was only a single permit for porch construction, which surprised me - I wouldn’t have expected it to be common, but I would have expected more than a single person to want to do it.

Interestingly however, Electric Wiring was not the most common permit with a positive unpaid balance. That went to “Signs”, followed by “Elevator Equipment” (which was only a distant 7th in total permits). In fact, Electric Wiring was only the fifth most common permit to have a positive unpaid balance. It should come as no surprise then that the Bayesian probability of a permit with a positive unpaid balance being for Signs was 0.3138, while the Bayesian probability of a permit with a positive unpaid balance being for Electric Wiring was only 0.0325. This suggests to me that there is some systematic difference between permits for signs and permits for electric wiring. Perhaps, with electric wiring being a more involved process than putting up a sign, those permits are only being pursued when the homeowner or construction company knows that they have the ability to pay for the entire project. Or perhaps there is an accounting or advertising reason for filing for permits for signs ahead of time and not paying until later.

Another interesting thing is the waived permits, where the most common permit type to have a waived amount is Easy Permit Process, with the second being Renovation/Alteration. The City of Chicago website says that the Easy Permit Process is “a streamlined permitting process for small, simple home and building improvement projects,” so perhaps it’s prominence in the waived permits (the Bayesian probability of a permit with a positive waived balance being an Easy Permit Process application is 0.3293, nearly a third) is a reflection of the City of Chicago going easy on these small time and small dollar filers.

Looking at the Bayesian Probabilities, I was able to create this table

| Balance Type | Positive/Negative/0 | Most Common Permit Type | Bayesian Probability
| --- | --- |  --- | --- |
Unpaid |Positive |Signs |0.3138 |
Unpaid |Zero |Electric Wiring |0.3563 |
Unpaid |Negative |Renovation/Alteration | 0.6316|
Paid |Positive |Electric Wiring |0.3550 |
Paid |Zero |Renovation/Alteration |0.3290 |
Paid |Negative |N/A |N/A |
Waived |Positive |Easy Permit Process |0.3293 |
Waived |Zero |Electric Wiring |0.3563 |
Waived |Negative |N/A |N/A |

It is unsurprising that the permit type with the greatest zero balance for Unpaid Balance and Waived Balance was Electric Wiring - this was the most common permit type, and we would expect most permits to not have an unpaid or waived balance. It is interesting that in our most “noteworthy” cases  - that is, permits with a positive unpaid balance or a positive waived balance, the Bayesian probability of the most common permit type is similar, at a little less than a third. Finally, the outlier (the Bayesian probability of Renovation/Alteration when there is a negative unpaid balance) simply reflects the small sample size - there is only a tiny amount of permits where the permit filer appears to have overpaid, in most cases presumably someone overestimating the potential cost of a renovation.

The code for this can be found in the pandasProgram.py file. You can also find the sparkDriver.py file, which was me using PySpark to try and load the data, calculate the percentile ranks of the unpaid balance for each permit, and convert the data to a Pandas dataframe. Unfortunately I ran into some errors with the conversion from Spark to Pandas (calculating the percentile ranks worked successfully) and in the interest of time I had to abandon the file. Another file is the pandasDriver.py, which I was using to load the data, trim it to save memory, save the data to a database, and execute a command to delete the permits with no unpaid balance from the database, so I could focus on those with a positive or negative unpaid balance. While this successfully trimmed the CSV file and connected to the local SQLite database, I ran into some issues getting the connection to work with the command, and once again in the interest of time had to abandon the file.

One possible extension, if I had the time and was able to get everything else working, would be to take advantage of the large amount of data and use a machine learning library, such as tensorflow, to try and classify the permit type based on other variables, such as outstanding balance, address, issue date, etc. While I am not sure how successful this would have been, there was more than enough data for large training and testing sets, and it would have been interesting to see how well it worked.
