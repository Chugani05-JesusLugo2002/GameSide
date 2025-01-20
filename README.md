# Gameside

## Models

### Game
- Title: CharField
- Slug: SlugField
- Description: TextField
- Cover: ImageField
- Price: Number
- Stock: Number
- Release Date: DateField
- PEGI: ChoicesField
- Category: FK
- Platforms: M2M

### Category
- Name: CharField
- Description: TextField
- Slug: SlugField
- Color: ???

### Platform
- Name: CharField
- Description: TextField
- Slug: SlugField

### Review
-  Comment: TextField
-  Rating: Range 0-5
-  Game: FK
-  User: FK

### Order
- User: FK
- Games: M2M
- Ordered At: DateField
- Paid: Boolean
- Total Price
- Key: CharField
