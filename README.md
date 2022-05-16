# The pastesian problem

*Author*: Luiz Suzana  
April 2022

This solution is the first project developed by the author as part of his journey at the [Mip Go][Mip Go] training 
program 
from 
[Mip Wise][Mip Wise].


It is going to solve the *pastesian* problem, whose basic statement is described in details [here][statement link], 
using the 
Mip Go 
framework, that is, by creating a tidy, tested and safe python package which may easily be deployed as a web 
application on [Mip Hub][mip hub], which is Mip Wise's app builder platform.

- Problem's basic statement: https://www.mipwise.com/use-cases/pastesian
- Mathematical formulation: [docs]
- Implementation: [scripts]
- Validating: [test pastesian]

## Statement

Pastesian is a family-owned pasta factory that is currently planning the production of lasagnas for the next 4 months.

Lasagnas are prepared and immediately frozen for distribution. They have some freezers in the factory where they can store inventory for several weeks before shipping them to the market.

Based on previous years’ selling, Pastesian expects demand of 200, 350, 150, and 250 lasagnas for months 1, 2, 3, and 4, respectively, which must be met exactly. Currently, Pastesian has only 50 lasagnas in inventory.

One tricky thing is that labor cost is going to increase over the next months because the factory is located in a 
tourist town where there are lots of temporary job opportunities during high season. This translates into a variable 
production cost of $ 5.50, $ 7.20, $ 8.80, and $ 10.90 dollars per lasagna for months 1, 2, 3, and 4, respectively.

In addition, electricity charges also vary throughout the season. As a result, the cost for keeping one lasagna in 
inventory from month 1 to 2 is $ 1.30, from month 2 to 3 is $ 1.95, from month 3 to 4 is $ 2.20, and from month 4 to 
the next horizon is $ 2.00

How should Pastesian plan its operations for these upcoming months?

### Additional Complexities

After analyzing the prescribed optimal solution, the Pastesian people realized that they would not be able to implement it for the following reasons.

- **Store capacity**: Currently, Pastesian doesn't have the capacity to store more than 200 lasagnas from one month to 
another.

- **Production capacity**: Pastesian has the capacity to produce at most 400 lasagnas each month. 


[Mip Go]: https://www.mipwise.com/mip-go
[Mip Wise]: https://www.mipwise.com/
[statement link]: https://www.mipwise.com/use-cases/pastesian
[mip hub]: https://www.mipwise.com/mip-hub
[docs]: docs/
[scripts]: pastesian/
[test pastesian]: test_pastesian/
