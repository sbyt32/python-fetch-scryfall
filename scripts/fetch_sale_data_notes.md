
### Build-your-own-query
```json
{
    "variants": [
        1, // Non-Foil
        2, // Foil
    ],
    "conditions": [
        1, // = Near Mint (NP)
        2, // = Lightly Played (LP)
        3, // = Moderately Played (MP)
        4, // = Heavily Played (HP)
        5, // = Damaged (DMG) 
        6, // = Unopened (SEAL) 
    ],

    "languages": [
        1, // = English   
        2, // = Chinese (Simplified) 
        3, // = Chinese (Traditional) 
        4, // = French   
        5, // = German   
        6, // = Italian   
        7, // = Japanese   
        8, // = Korean  
        9, // = Portuguese   
        10, // = Russian   
        11, // = Spanish   
    ],
    "listingType": "All",
    // Listing Type: 
        // "All"                    = Shows all listings
        // "ListingWithPhotos"      = Shows only listings with photos
        // "ListingWithoutPhotos"   = Shows only listings without photos
    "limit": 25, // 1-25 0 returns 10, 
    "offset":0, // Self Explanatory
}
```