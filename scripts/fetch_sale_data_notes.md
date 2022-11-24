
### Build-your-own-query
```json
{
    "variants": [
        1,
        2
    ],
    // Variants = [0 (non-foil), 1 (foil)]
    "conditions": [
        1,
        2,
        3,
        4,
        5,
        6
    ],
    // Conditions = [
    //     1    = Near Mint (NP)
    //     2    = Lightly Played (LP)
    //     3    = Moderately Played (MP)
    //     4    = Heavily Played (HP) 
    //     5    = Damaged (DMG) 
    //     6    = Unopened (SEAL) 
    // ]
    "languages": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8
    ],
    // Languages: [
    //     1    = English   
    //     2    = Chinese (Simplified)   
    //     3    = Chinese (Traditional)   
    //     4    = French   
    //     5    = German   
    //     6    = Italian   
    //     7    = Japanese   
    //     8    = Korean   
    //     9    = Portuguese   
    //     10   = Russian   
    //     11   = Spanish   
    // ],
    "listingType": "ListingWithPhotos",
    // Listing Type: 
        // "All                     = Shows all listings
        // "ListingWithPhotos"      = Shows only listings with photos
        // "ListingWithoutPhotos"   = Shows only listings without photos
    "limit": 25,
    "offset":0,
    
}
```