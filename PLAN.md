# Project Plan

## Goal

Build a simple tool that estimates a used car's asking price from details such as its year, mileage, fuel, transmission, type, and condition. We will compare two prediction methods and explain the tool's limits.

## Steps

| Step | What | Who | Deadline |
|---|---|---|---|
| Presentation plan | Explain the problem, why an estimator is useful, and how we plan to finish. | ? | Monday 16 November |
| Clean the data | Fix or remove records that are missing, invalid, or outside the project's scope. | ? | Friday 20 November |
| Choose features | Select which car details the model will use. These details are called *features*. | ? | Saturday 21 November |
| Simple model | Train linear regression, a basic method that estimates price using patterns between car details and price. | ? | Monday 23 November |
| Stronger model | Train a random forest, a method that combines many decision trees (sets of if/then choices). | ? | Wednesday 25 November |
| Compare models | Compare their average error in dollars. This is the average amount their estimates differ from the listed prices. | ? | Thursday 26 November |
| Build a simple app | Let a user enter car details and see an estimated price. | ? | Saturday 28 November |
| Write the final README | Explain the project's purpose, how to run it, and its limitations. | ? | Sunday 29 November |
| Final testing | Check that the finished project runs and the app gives an estimate. | ? | Monday 30 November |

## Risks and limitations

- The data is messy: some prices or mileage values may be unrealistic, some details are missing, and model names are spelled in many different ways.
- The listed prices are asking prices, not confirmed sale prices. The estimate may not match what a car actually sells for.
- The data covers US listings only, so the estimator may not fit cars or prices in other countries.
- We have not trained or compared the models yet, so we do not know how accurate their estimates will be.
