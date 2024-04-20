# The Witches Pantry

The UK throws away around 9.5 million tonnes of food waste in a single year and around 60% of that is from household waste.

The Witches Pantry is my idea to help reduce food waste by being able to check at any time when an item in your fridge/cupboards is going to expire. By being able to check within the day/week/two weeks/three weeks when items in your pantry are expiring we will be able to have better control over the waste we produce.

![image of live site on multiple devices](<readme images/responsive-image.webp>)

## How To Use Functions

To log in please use the username and password provided.

The app is case sensitive so be sure to type the username and password correctly.

Once logged in you will be presented with 7 options, type the number of the function you would like to use and press enter.

![image of the apps main menu](<readme images/main-menu.png>)

### 1: Enter Add Item

To add an item to your pantry simply enter the item name and then the use by date and press enter. The item will now be logged to your pantry and you will be brought back to the main menu.

![image of add item function](<readme images/add-item.png>)

### 2: Show Items Expiring Today

Once you select this function it will show you any items with the use by date of the current date.

![image of the expiring today items](<readme images/expiring-today.png>)

### 3: Show Items Expiring in One Week
Once you select this function it will show you any items with the use buy date within the next week.

![image of items expiring in one week](<readme images/expire-one-week.png>)

### 4: Show Items Expiring in Two Weeks
Once you select this function it will show you any items with the use buy date within the next two weeks.

![image of items expiring in two weeks](<readme images/expire-two-weeks.png>)

### 5: Show Items Expiring in Three Weeks
Once you select this function it will show you any items with the use buy date within the next three weeks.

![image of items expiring in three weeks](<readme images/expire-three-weeks.png>)

### 6: Delete Item

When you select to delete an item it will automatically show you items that have expired. From here you can simply enter the item name in the input area and press enter. This is case sensitive and will not delete unless entered as seen.

![image of delete item function](<readme images/delete-item.png>)

### 7: Log Out

When this function is selected it will end your session and return to the login screen.

## Future Developments

Ideas to impliment in the future.

- For the app to find you recipes containing the items that are expiring in the next week.
- Create an account function for more users.

## Testing

I have manually tested this app by doing the following:

- Passed the code through PEP8 linter.
- I have manually tested by entering incorrect values in python terminal and Heroku.

### Bugs

**Solved Bugs**

- Whilst building this app i keep getting errors updating items to the google sheet. I fixed this by saving the username globally and then assigning that to function to call the sheet that was being updated meaning either user account i set up could now be updated.
- I also had a large issue with the date as it is set to the american standard mm/dd/yy by default. I managed to correct this by formatting the date with %d/%m/%Y. This now means I have better control over searches and could now bring up lists for items expiring and items expired.

### Validator Testing

PEP8: No errors returned form https://pep8ci.herokuapp.com/

![image of pep8 linter showing no issues with the code](<readme images/linter-pass.png>)

## Deployment

This app  was deployed using Code Institute's mock terminal for Heroku.

Steps taken for deployment
- Clone the repository
- Create Heroku app
- Set Python and NodeJS buidbacks
- Link repository with Heroku
- Click Deploy


## Credits

- Code Institute for the deployment terminal
- login code = shawcode https://www.youtube.com/watch?v=L2i6lELbNI0
- witches pantry header = ASC11  https://textkool.com/
- Delftstack for clear console code https://www.delftstack.com/howto/python/python-clear-console/