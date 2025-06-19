import json
ITEM_MESSAGES: list[tuple[int, str]] = [
    (0x0001, "\x08\x06\x30\x05\x41TEXT ID ERROR!\x05\x40"),
    (0x9001, "\x08\x13\x2DYou borrowed a \x05\x41Pocket Egg\x05\x40!\x01A Pocket Cucco will hatch from\x01it overnight. Be sure to give it\x01back."),
    (0x0002, "\x08\x13\x2FYou returned the Pocket Cucco\x01and got \x05\x41Cojiro\x05\x40 in return!\x01Unlike other Cuccos, Cojiro\x01rarely crows."),
    (0x0003, "\x08\x13\x30You got an \x05\x41Odd Mushroom\x05\x40!\x01It is sure to spoil quickly! Take\x01it to the Kakariko Potion Shop."),
    (0x0004, "\x08\x13\x31You received an \x05\x41Odd Potion\x05\x40!\x01It may be useful for something...\x01Hurry to the Lost Woods!"),
    (0x0005, "\x08\x13\x32You returned the Odd Potion \x01and got the \x05\x41Poacher's Saw\x05\x40!\x01The young punk guy must have\x01left this."),
    (0x0007, "\x08\x13\x48You got a \x01\x05\x41Deku Seeds Bullet Bag\x05\x40.\x01This bag can hold up to \x05\x4640\x05\x40\x01slingshot bullets."),
    (0x0008, "\x08\x13\x33You traded the Poacher's Saw \x01for a \x05\x41Broken Goron's Sword\x05\x40!\x01Visit Biggoron to get it repaired!"),
    (0x0009, "\x08\x13\x34You checked in the Broken \x01Goron's Sword and received a \x01\x05\x41Prescription\x05\x40!\x01Go see King Zora!"),
    (0x000A, "\x08\x13\x37The Biggoron's Sword...\x01You got a \x05\x41Claim Check \x05\x40for it!\x01You can't wait for the sword!"),
    (0x000B, "\x08\x13\x2EYou got a \x05\x41Pocket Cucco, \x05\x40one\x01of Anju's prized hens! It fits \x01in your pocket."),
    (0x000C, "\x08\x13\x3DYou got the \x05\x41Biggoron's Sword\x05\x40!\x01This blade was forged by a \x01master smith and won't break!"),
    (0x000D, "\x08\x13\x35You used the Prescription and\x01received an \x05\x41Eyeball Frog\x05\x40!\x01Be quick and deliver it to Lake \x01Hylia!"),
    (0x000E, "\x08\x13\x36You traded the Eyeball Frog \x01for the \x05\x41World's Finest Eye Drops\x05\x40!\x01Hurry! Take them to Biggoron!"),
    (0x0010, "\x08\x13\x25You got a \x05\x41Skull Mask\x05\x40.\x01You feel like a monster while you\x01wear this mask!"),
    (0x0011, "\x08\x13\x26You got a \x05\x41Spooky Mask\x05\x40.\x01You can scare many people\x01with this mask!"),
    (0x0012, "\x08\x13\x24You got a \x05\x41Keaton Mask\x05\x40.\x01You'll be a popular guy with\x01this mask on!"),
    (0x0013, "\x08\x13\x27You got a \x05\x41Bunny Hood\x05\x40.\x01The hood's long ears are so\x01cute!"),
    (0x0014, "\x08\x13\x28You got a \x05\x41Goron Mask\x05\x40.\x01It will make your head look\x01big, though."),
    (0x0015, "\x08\x13\x29You got a \x05\x41Zora Mask\x05\x40.\x01With this mask, you can\x01become one of the Zoras!"),
    (0x0016, "\x08\x13\x2AYou got a \x05\x41Gerudo Mask\x05\x40.\x01This mask will make you look\x01like...a girl?"),
    (0x0017, "\x08\x13\x2BYou got a \x05\x41Mask of Truth\x05\x40.\x01Show it to many people!"),
    (0x0030, "\x08\x13\x06You found the \x05\x41Fairy Slingshot\x05\x40!"),
    (0x0031, "\x08\x13\x03You found the \x05\x41Fairy Bow\x05\x40!"),
    (0x0035, "\x08\x13\x0EYou found the \x05\x41Boomerang\x05\x40!"),
    (0x0036, "\x08\x13\x0AYou found the \x05\x41Hookshot\x05\x40!\x01It's a spring-loaded chain that\x01you can cast out to hook things."),
    (0x0038, "\x08\x13\x11You found the \x05\x41Megaton Hammer\x05\x40!\x01It's so heavy, you need to\x01use two hands to swing it!"),
    (0x0039, "\x08\x13\x0FYou found the \x05\x41Lens of Truth\x05\x40!\x01Mysterious things are hidden\x01everywhere!"),
    (0x003A, "\x08\x13\x08You found the \x05\x41Ocarina of Time\x05\x40!\x01It glows with a mystical light..."),
    (0x003C, "\x08\x13\x67You received the \x05\x41Fire\x01Medallion\x05\x40!\x01Darunia awakens as a Sage and\x01adds his power to yours!"),
    (0x003D, "\x08\x13\x68You received the \x05\x43Water\x01Medallion\x05\x40!\x01Ruto awakens as a Sage and\x01adds her power to yours!"),
    (0x003E, "\x08\x13\x66You received the \x05\x42Forest\x01Medallion\x05\x40!\x01Saria awakens as a Sage and\x01adds her power to yours!"),
    (0x003F, "\x08\x13\x69You received the \x05\x46Spirit\x01Medallion\x05\x40!\x01Nabooru awakens as a Sage and\x01adds her power to yours!"),
    (0x0040, "\x08\x13\x6BYou received the \x05\x44Light\x01Medallion\x05\x40!\x01Rauru the Sage adds his power\x01to yours!"),
    (0x0041, "\x08\x13\x6AYou received the \x05\x45Shadow\x01Medallion\x05\x40!\x01Impa awakens as a Sage and\x01adds her power to yours!"),
    (0x0042, "\x08\x13\x14You got an \x05\x41Empty Bottle\x05\x40!\x01You can put something in this\x01bottle."),
    (0x0048, "\x08\x13\x10You got a \x05\x41Magic Bean\x05\x40!\x01Find a suitable spot for a garden\x01and plant it."),
    (0x9048, "\x08\x13\x10You got a \x05\x41Pack of Magic Beans\x05\x40!\x01Find suitable spots for a garden\x01and plant them."),
    (0x004A, "\x08\x13\x07You received the \x05\x41Fairy Ocarina\x05\x40!\x01This is a memento from Saria."),
    (0x004B, "\x08\x13\x3DYou got the \x05\x42Giant's Knife\x05\x40!\x01Hold it with both hands to\x01attack! It's so long, you\x01can't use it with a \x05\x44shield\x05\x40."),
    (0x004E, "\x08\x13\x40You found the \x05\x44Mirror Shield\x05\x40!\x01The shield's polished surface can\x01reflect light or energy."),
    (0x004F, "\x08\x13\x0BYou found the \x05\x41Longshot\x05\x40!\x01It's an upgraded Hookshot.\x01It extends \x05\x41twice\x05\x40 as far!"),
    (0x0052, "\x08You got a \x05\x42Magic Jar\x05\x40!\x01Your Magic Meter is filled!"),
    (0x0053, "\x08\x13\x45You got the \x05\x41Iron Boots\x05\x40!\x01So heavy, you can't run.\x01So heavy, you can't float."),
    (0x0054, "\x08\x13\x46You got the \x05\x41Hover Boots\x05\x40!\x01With these mysterious boots\x01you can hover above the ground."),
    (0x0056, "\x08\x13\x4BYou upgraded your quiver to a\x01\x05\x41Big Quiver\x05\x40!\x01Now you can carry more arrows-\x01\x05\x4640 \x05\x40in total!"),
    (0x0057, "\x08\x13\x4CYou upgraded your quiver to\x01the \x05\x41Biggest Quiver\x05\x40!\x01Now you can carry to a\x01maximum of \x05\x4650\x05\x40 arrows!"),
    (0x0058, "\x08\x13\x4DYou found a \x05\x41Bomb Bag\x05\x40!\x01You found \x05\x4120 Bombs\x05\x40 inside!"),
    (0x0059, "\x08\x13\x4EYou got a \x05\x41Big Bomb Bag\x05\x40!\x01Now you can carry more \x01Bombs, up to a maximum of \x05\x4630\x05\x40!"),
    (0x005A, "\x08\x13\x4FYou got the \x01\x05\x41Biggest Bomb Bag\x05\x40!\x01Now, you can carry up to \x01\x05\x4640\x05\x40 Bombs!"),
    (0x005B, "\x08\x13\x51You found the \x05\x43Silver Gauntlets\x05\x40!\x01You feel the power to lift\x01big things with it!"),
    (0x005C, "\x08\x13\x52You found the \x05\x43Golden Gauntlets\x05\x40!\x01You can feel even more power\x01coursing through your arms!"),
    (0x005E, "\x08\x13\x56You got an \x05\x43Adult's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46200\x05\x40 \x05\x46Rupees\x05\x40."),
    (0x005F, "\x08\x13\x57You got a \x05\x43Giant's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46500\x05\x40 \x05\x46Rupees\x05\x40."),
    (0x0060, "\x08\x13\x77You found a \x05\x41Small Key\x05\x40!\x01This key will open a locked \x01door. You can use it only\x01in this dungeon."),
    (0x0066, "\x08\x13\x76You found the \x05\x41Dungeon Map\x05\x40!\x01It's the map to this dungeon."),
    (0x0067, "\x08\x13\x75You found the \x05\x41Compass\x05\x40!\x01Now you can see the locations\x01of many hidden things in the\x01dungeon!"),
    (0x0068, "\x08\x13\x6FYou obtained the \x05\x41Stone of Agony\x05\x40!\x01If you equip a \x05\x44Rumble Pak\x05\x40, it\x01will react to nearby...secrets."),
    (0x0069, "\x08\x13\x23You received \x05\x41Zelda's Letter\x05\x40!\x01Wow! This letter has Princess\x01Zelda's autograph!"),
    (0x006C, "\x08\x13\x49Your \x05\x41Deku Seeds Bullet Bag \x01\x05\x40has become bigger!\x01This bag can hold \x05\x4650\x05\x41 \x05\x40bullets!"),
    (0x006F, "\x08You got a \x05\x42Green Rupee\x05\x40!\x01That's \x05\x42one Rupee\x05\x40!"),
    (0x0070, "\x08\x13\x04You got the \x05\x41Fire Arrow\x05\x40!\x01If you hit your target,\x01it will catch fire."),
    (0x0071, "\x08\x13\x0CYou got the \x05\x43Ice Arrow\x05\x40!\x01If you hit your target,\x01it will freeze."),
    (0x0072, "\x08\x13\x12You got the \x05\x44Light Arrow\x05\x40!\x01The light of justice\x01will smite evil!"),
    (0x0079, "\x08\x13\x50You got the \x05\x41Goron's Bracelet\x05\x40!\x01Now you can pull up Bomb\x01Flowers."),
    (0x007B, "\x08\x13\x70You obtained the \x05\x41Gerudo's \x01Membership Card\x05\x40!\x01You can get into the Gerudo's\x01training ground."),
    (0x0080, "\x08\x13\x6CYou got the \x05\x42Kokiri's Emerald\x05\x40!\x01This is the Spiritual Stone of \x01Forest passed down by the\x01Great Deku Tree."),
    (0x0081, "\x08\x13\x6DYou obtained the \x05\x41Goron's Ruby\x05\x40!\x01This is the Spiritual Stone of \x01Fire passed down by the Gorons!"),
    (0x0082, "\x08\x13\x6EYou obtained \x05\x43Zora's Sapphire\x05\x40!\x01This is the Spiritual Stone of\x01Water passed down by the\x01Zoras!"),
    (0x0090, "\x08\x13\x00Now you can pick up \x01many \x05\x41Deku Sticks\x05\x40!\x01You can carry up to \x05\x4620\x05\x40 of them!"),
    (0x0091, "\x08\x13\x00You can now pick up \x01even more \x05\x41Deku Sticks\x05\x40!\x01You can carry up to \x05\x4630\x05\x40 of them!"),
    (0x0098, "\x08\x13\x1AYou got \x05\x41Lon Lon Milk\x05\x40!\x01This milk is very nutritious!\x01There are two drinks in it."),
    (0x0099, "\x08\x13\x1BYou found \x05\x41Ruto's Letter\x05\x40 in a\x01bottle! Show it to King Zora."),
    (0x9099, "\x08\x13\x1BYou found \x05\x41a letter in a bottle\x05\x40!\x01You remove the letter from the\x01bottle, freeing it for other uses."),
    (0x009A, "\x08\x13\x21You got a \x05\x41Weird Egg\x05\x40!\x01Feels like there's something\x01moving inside!"),
    (0x00A4, "\x08\x13\x3BYou got the \x05\x42Kokiri Sword\x05\x40!\x01This is a hidden treasure of\x01the Kokiri."),
    (0x00A7, "\x08\x13\x01Now you can carry\x01many \x05\x41Deku Nuts\x05\x40!\x01You can hold up to \x05\x4630\x05\x40 nuts!"),
    (0x00A8, "\x08\x13\x01You can now carry even\x01more \x05\x41Deku Nuts\x05\x40! You can carry\x01up to \x05\x4640\x05\x41 \x05\x40nuts!"),
    (0x00AD, "\x08\x13\x05You got \x05\x41Din's Fire\x05\x40!\x01Its fireball engulfs everything!"),
    (0x00AE, "\x08\x13\x0DYou got \x05\x42Farore's Wind\x05\x40!\x01This is warp magic you can use!"),
    (0x00AF, "\x08\x13\x13You got \x05\x43Nayru's Love\x05\x40!\x01Cast this to create a powerful\x01protective barrier."),
    (0x00B4, "\x08You got a \x05\x41Gold Skulltula Token\x05\x40!\x01You've collected \x05\x41\x19\x05\x40 tokens in total."),
    (0x00B5, "\x08You destroyed a \x05\x41Gold Skulltula\x05\x40.\x01You got a token proving you \x01destroyed it!"), #Unused
    (0x00C2, "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Collect four pieces total to get\x01another Heart Container."),
    (0x90C2, "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You are already at\x01maximum health."),
    (0x00C3, "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01So far, you've collected two \x01pieces."),
    (0x00C4, "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Now you've collected three \x01pieces!"),
    (0x00C5, "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You've completed another Heart\x01Container!"),
    (0x00C6, "\x08\x13\x72You got a \x05\x41Heart Container\x05\x40!\x01Your maximum life energy is \x01increased by one heart."),
    (0x90C6, "\x08\x13\x72You got a \x05\x41Heart Container\x05\x40!\x01You are already at\x01maximum health."),
    (0x00C7, "\x08\x13\x74You got the \x05\x41Boss Key\x05\x40!\x01Now you can get inside the \x01chamber where the Boss lurks."),
    (0x00CC, "\x08You got a \x05\x43Blue Rupee\x05\x40!\x01That's \x05\x43five Rupees\x05\x40!"),
    (0x00CD, "\x08\x13\x53You got the \x05\x43Silver Scale\x05\x40!\x01You can dive deeper than you\x01could before."),
    (0x00CE, "\x08\x13\x54You got the \x05\x43Golden Scale\x05\x40!\x01Now you can dive much\x01deeper than you could before!"),
    (0x00DD, "\x08You mastered the secret sword\x01technique of the \x05\x41Spin Attack\x05\x40!"),
    (0x00E4, "\x08You can now use \x05\x42Magic\x05\x40!"),
    (0x00E5, "\x08Your \x05\x44defensive power\x05\x40 is enhanced!"),
    (0x00E8, "\x08Your magic power has been \x01enhanced! Now you have twice\x01as much \x05\x41Magic Power\x05\x40!"),
    (0x00E9, "\x08Your defensive power has been \x01enhanced! Damage inflicted by \x01enemies will be \x05\x41reduced by half\x05\x40."),
    (0x00F0, "\x08You got a \x05\x41Red Rupee\x05\x40!\x01That's \x05\x41twenty Rupees\x05\x40!"),
    (0x00F1, "\x08You got a \x05\x45Purple Rupee\x05\x40!\x01That's \x05\x45fifty Rupees\x05\x40!"),
    (0x00F2, "\x08You got a \x05\x46Huge Rupee\x05\x40!\x01This Rupee is worth a whopping\x01\x05\x46two hundred Rupees\x05\x40!"),
    (0x00F4, "\x08\x05\x44Loser!\x05\x40\x04\x08You found only \x05\x42one Rupee\x05\x40.\x01You are not very lucky."),
    (0x00F5, "\x08\x05\x44Loser!\x05\x40\x04\x08You found \x05\x43five Rupees\x05\x40.\x01Even so, you are not very lucky."),
    (0x00F6, "\x08\x05\x44Loser!\x05\x40\x04\x08You found \x05\x41twenty Rupees\x05\x40.\x01Your last selection was a mistake,\x01wasn't it! How frustrating!"),
    (0x00F7, "\x08\x05\x41Winner!\x05\x40\x04\x08You found \x05\x46fifty Rupees\x05\x40.\x01You are a genuinely lucky guy!"),
    (0x00FA, "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Collect four pieces total to get\x01another Heart Container."),
    (0x00FB, "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01So far, you've collected two \x01pieces."),
    (0x00FC, "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Now you've collected three \x01pieces!"),
    (0x00FD, "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You've completed another Heart\x01Container!"),
    (0x90FA, "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You are already at\x01maximum health."),
    #(0x6074, "\x08Oh, that's too bad.\x04\x08If you change your mind, please\x01come back again!\x04\x08The mark that will lead you to the\x01Spirit Temple is the \x05\x41flag on\x01the left \x05\x40outside the shop."),
    (0x9002, "\x08You are a \x05\x43FOOL\x05\x40!"),
    (0x9003, "\x08You found a piece of the \x05\x41Triforce\x05\x40!"),
    (0x9019, "\x08\x13\x09You found a \x05\x41Bombchu Bag\x05\x40!\x01It has some \x05\x41Bombchus\x05\x40 inside!\x01Find more in tall grass."),
    (0x901A, "\x08You can't buy Bombchus without a\x01\x05\x41Bombchu Bag\x05\x40!"),
    (0x908C, "\x08You got the\x01\x05\x41Ocarina A Button!\x05\x40\x01You can now play \x9F on the Ocarina!"),
    (0x908D, "\x08You got the\x01\x05\x41Ocarina C-up Button!\x05\x40\x01You can now play \xA5 on the Ocarina!"),
    (0x908E, "\x08You got the\x01\x05\x41Ocarina C-down Button!\x05\x40\x01You can now play \xA6 on the Ocarina!"),
    (0x908F, "\x08You got the\x01\x05\x41Ocarina C-left Button!\x05\x40\x01You can now play \xA7 on the Ocarina!"),
    (0x9090, "\x08You got the\x01\x05\x41Ocarina C-right Button!\x05\x40\x01You can now play \xA8 on the Ocarina!"),
    (0x9091, "\x08\x06\x28You have learned the\x01\x06\x2F\x05\x42Minuet of Forest\x05\x40!"),
    (0x9092, "\x08\x06\x28You have learned the\x01\x06\x37\x05\x41Bolero of Fire\x05\x40!"),
    (0x9093, "\x08\x06\x28You have learned the\x01\x06\x29\x05\x43Serenade of Water\x05\x40!"),
    (0x9094, "\x08\x06\x28You have learned the\x01\x06\x2D\x05\x46Requiem of Spirit\x05\x40!"),
    (0x9095, "\x08\x06\x28You have learned the\x01\x06\x28\x05\x45Nocturne of Shadow\x05\x40!"),
    (0x9096, "\x08\x06\x28You have learned the\x01\x06\x32\x05\x44Prelude of Light\x05\x40!"),
    # 0x9097 and 0x9098 unused
    # 0x9099 used above
    (0x909A, "\x08\x06\x15You've learned \x05\x43Zelda's Lullaby\x05\x40!"),
    (0x909B, "\x08\x06\x11You've learned \x05\x41Epona's Song\x05\x40!"),
    (0x909C, "\x08\x06\x14You've learned \x05\x42Saria's Song\x05\x40!"),
    (0x909D, "\x08\x06\x0BYou've learned the \x05\x46Sun's Song\x05\x40!"),
    (0x909E, "\x08\x06\x05You've learned the \x05\x44Song of Time\x05\x40!"),
    (0x909F, "\x08You've learned the \x05\x45Song of Storms\x05\x40!"),
    (0x90A0, "\x08\x13\x15You got a \x05\x41Red Potion\x05\x40!\x01It will restore your health"),
    (0x90A1, "\x08\x13\x16You got a \x05\x42Green Potion\x05\x40!\x01It will restore your magic."),
    (0x90A2, "\x08\x13\x17You got a \x05\x43Blue Potion\x05\x40!\x01It will recover your health\x01and magic."),
    (0x90A3, "\x08\x13\x18You caught a \x05\x41Fairy\x05\x40 in a bottle!\x01It will revive you\x01the moment you run out of life \x01energy."),
    (0x90A4, "\x08\x13\x19You got a \x05\x41Fish\x05\x40!\x01It looks so fresh and\x01delicious!"),
    (0x90A5, "\x08\x13\x1CYou put a \x05\x44Blue Fire\x05\x40\x01into the bottle!\x01This is a cool flame you can\x01use on red ice."),
    (0x90A6, "\x08\x13\x1DYou put a \x05\x41Bug \x05\x40in the bottle!\x01This kind of bug prefers to\x01live in small holes in the ground."),
    (0x90A7, "\x08\x13\x1EYou put a \x05\x41Big Poe \x05\x40in a bottle!\x01Let's sell it at the \x05\x41Ghost Shop\x05\x40!\x01Something good might happen!"),
    (0x90A8, "\x08\x13\x20You caught a \x05\x41Poe \x05\x40in a bottle!\x01Something good might happen!"),
    (0x90A9, "\x08\x13\x02You got \x05\x41Bombs\x05\x40!\x01If you see something\x01suspicious, bomb it!"),
    (0x90AA, "\x08\x13\x01You got a \x05\x41Deku Nut\x05\x40!"),
    (0x90AB, "\x08\x13\x09You got \x05\x41Bombchus\x05\x40!"),
    (0x90AC, "\x08\x13\x00You got a \x05\x41Deku Stick\x05\x40!"),
    (0x90AD, "\x08\x13\x3EYou got a \x05\x44Deku Shield\x05\x40!"),
    (0x90AE, "\x08\x13\x3FYou got a \x05\x44Hylian Shield\x05\x40!"),
    (0x90AF, "\x08\x13\x42You got a \x05\x41Goron Tunic\x05\x40!\x01Going to a hot place? No worry!"),
    (0x90B0, "\x08\x13\x43You got a \x05\x43Zora Tunic\x05\x40!\x01Wear it, and you won't drown\x01underwater."),
    (0x90B1, "\x08You got a \x05\x45Recovery Heart\x05\x40!\x01Your life energy is recovered!"),
    (0x90B2, "\x08You got a \x05\x46bundle of arrows\x05\x40!"),
    (0x90B3, "\x08\x13\x58You got \x05\x41Deku Seeds\x05\x40!\x01Use these as bullets\x01for your Slingshot."),
    (0x90B4, "\x08You found a \x05\x41fairy\x05\x40!\x01Your health has been restored!"),
    (0x90B5, "\x08You found \x05\x43literally nothing\x05\x40!"),
]

KEYSANITY_MESSAGES: list[tuple[int, str]] = [
    (0x001C, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09"),
    (0x0006, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09"),
    (0x001D, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09"),
    (0x001E, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x002A, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x0061, "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x0062, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09"),
    (0x0063, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x41Dodongo's Cavern\x05\x40!\x09"),
    (0x0064, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x43Jabu Jabu's Belly\x05\x40!\x09"),
    (0x0065, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09"),
    (0x007C, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09"),
    (0x007D, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09"),
    (0x007E, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x007F, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x0087, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09"),
    (0x0088, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09"),
    (0x0089, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x41Dodongo's Cavern\x05\x40!\x09"),
    (0x008A, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x43Jabu Jabu's Belly\x05\x40!\x09"),
    (0x008B, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09"),
    (0x008C, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09"),
    (0x008E, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09"),
    (0x008F, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x0092, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09"),
    (0x0093, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09"),
    (0x0094, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09"),
    (0x0095, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09"),
    (0x009B, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09"),
    (0x009F, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Gerudo Training\x01Ground\x05\x40!\x09"),
    (0x00A0, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Thieves' Hideout\x05\x40!\x09"),
    (0x00A1, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x00A2, "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09"),
    (0x00A3, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x00A5, "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09"),
    (0x00A6, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x00A9, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x00F3, "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x44Treasure Box Shop\x05\x40!\x09"),
    # 0x9019 and 0x901A used above
    # Silver Rupee Messages with count.
    (0x901B, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01staircase room in \x05\x41Dodongo's Cavern\x05\x40!\x01You have found \x05\x41\xF0\x00\x05\x40 so far!\x09"),
    (0x901C, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44spinning scythe room\x05\x40 in the \x05\x44Ice\x01Cavern\x05\x40! You have found \x05\x41\xF0\x01\x05\x40 so far!\x09"),
    (0x901D, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43push block room\x05\x40 in the \x05\x44Ice Cavern\x05\x40!\x01You have found \x05\x41\xF0\x02\x05\x40 so far!\x09"),
    (0x901E, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01basement in the \x05\x45Bottom of the Well\x05\x40!\x01You have found \x05\x41\xF0\x03\x05\x40 so far!\x09"),
    (0x901F, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42scythe shortcut room\x05\x40 in the \x05\x45Shadow\x01Temple\x05\x40! You have found \x05\x41\xF0\x04\x05\x40 so far!\x09"),
    (0x9020, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44invisible blade room\x05\x40 in the \x05\x45Shadow\x01Temple\x05\x40! You have found \x05\x41\xF0\x05\x05\x40 so far!\x09"),
    (0x9021, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46huge pit\x05\x40 in the \x05\x45Shadow Temple\x05\x40!\x01You have found \x05\x41\xF0\x06\x05\x40 so far!\x09"),
    (0x9022, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01room with \x05\x45invisible spikes\x05\x40 in the\x01\x05\x45Shadow Temple\x05\x40!\x01You have found \x05\x41\xF0\x07\x05\x40 so far!\x09"),
    (0x9023, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46sloped room\x05\x40 in the \x05\x46Gerudo Training\x01Ground\x05\x40! You have found \x05\x41\xF0\x08\x05\x40 so far!\x09"),
    (0x9024, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x41lava\x01room\x05\x40 in the \x05\x46Gerudo Training Ground\x05\x40!\x01You have found \x05\x41\xF0\x09\x05\x40 so far!\x09"),
    (0x9025, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43water room\x05\x40 in the \x05\x46Gerudo Training\x01Ground\x05\x40! You have found \x05\x41\xF0\x0A\x05\x40 so far!\x09"),
    (0x9026, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x41torch room\x05\x40 in the child side of the\x01\x05\x46Spirit Temple\x05\x40! You have found \x05\x41\xF0\x0B\x05\x40\x01so far!\x09"),
    (0x9027, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42boulder room\x05\x40 in the adult side of the\x01\x05\x46Spirit Temple\x05\x40! You have found \x05\x41\xF0\x0C\x05\x40\x01so far!\x09"),
    (0x9028, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44lobby and adult side\x05\x40 of the \x05\x46Spirit\x01Temple\x05\x40! You have found \x05\x41\xF0\x0D\x05\x40 so far!\x09"),
    (0x9029, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x46sun\x01block room\x05\x40 in the \x05\x46Spirit Temple\x05\x40!\x01You have found \x05\x41\xF0\x0E\x05\x40 so far!\x09"),
    (0x902A, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43climbable wall\x05\x40 in the \x05\x46Spirit Temple\x05\x40!\x01You have found \x05\x41\xF0\x0F\x05\x40 so far!\x09"),
    (0x902B, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46Spirit Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x10\x05\x40 so far!\x09"),
    (0x902C, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44Light Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x11\x05\x40 so far!\x09"),
    (0x902D, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x41Fire\x01Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x12\x05\x40 so far!\x09"),
    (0x902E, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x45Shadow Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x13\x05\x40 so far!\x09"),
    (0x902F, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43Water Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x14\x05\x40 so far!\x09"),
    (0x9030, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42Forest Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x01You have found \x05\x41\xF0\x15\x05\x40 so far!\x09"),
    # Silver Rupee messages when all have been collected. IDs are 0x16 after the base messages and calculated in resolve_text_id_silver_rupees. Also used for silver rupee pouches
    (0x9031, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the staircase room in\x01\x05\x41Dodongo's Cavern\x05\x40!\x09"),
    (0x9032, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44spinning scythe room\x05\x40\x01in the \x05\x44Ice Cavern\x05\x40!\x09"),
    (0x9033, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43push block room\x05\x40 in\x01the \x05\x44Ice Cavern\x05\x40!\x09"),
    (0x9034, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the basement in the\x01\x05\x45Bottom of the Well\x05\x40!\x09"),
    (0x9035, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42scythe shortcut room\x05\x40\x01in the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x9036, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44invisible blade room\x05\x40 in\x01the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x9037, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46huge pit\x05\x40 in the\x01\x05\x45Shadow Temple\x05\x40!\x09"),
    (0x9038, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the room with \x05\x45invisible\x01spikes\x05\x40 in the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x9039, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46sloped room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40!\x09"),
    (0x903A, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41lava room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40!\x09"),
    (0x903B, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43water room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40!\x09"),
    (0x903C, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41torch room\x05\x40 in the\x01child side of the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x903D, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42boulder room\x05\x40 in the\x01adult side of the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x903E, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44lobby and adult side\x05\x40\x01of the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x903F, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46sun block room\x05\x40 in the\x01\x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9040, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43climbable wall\x05\x40 in the\x01\x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9041, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46Spirit Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40!\x09"),
    (0x9042, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44Light Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40!\x09"),
    (0x9043, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41Fire Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40!\x09"),
    (0x9044, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x45Shadow Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9045, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43Water Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9046, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42Forest Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40!\x09"),
    # 0x9048 used above
    # Silver Rupee messages for MQ dungeons when all have been collected. Offset 0x2E from the base messages.
    (0x9049, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the staircase room in\x01\x05\x41Dodongo's Cavern\x05\x40! The way to the\x01hanging bridge is open!\x09"),
    # 0x904A, 0x904B, and 0x904C unused
    (0x904D, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42scythe shortcut room\x05\x40\x01in the \x05\x45Shadow Temple\x05\x40! Now you can\x01access the \x05\x42chest\x05\x40 there!\x09"),
    (0x904E, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44invisible blade room\x05\x40 in\x01the \x05\x45Shadow Temple\x05\x40! Now you can\x01access the \x05\x44chest\x05\x40 there!\x09"),
    (0x904F, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46huge pit\x05\x40 in the\x01\x05\x45Shadow Temple\x05\x40! A \x05\x46chest\x05\x40 has\x01appeared!\x09"),
    (0x9050, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the room with \x05\x45invisible\x01spikes\x05\x40 in the \x05\x45Shadow Temple\x05\x40! The\x01way to the \x05\x45Stalfos room\x05\x40 is open!\x09"),
    (0x9051, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46sloped room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! The way to\x01the room with the \x05\x46heavy block\x05\x40 is\x04open!\x09"),
    (0x9052, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41lava room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! The way to\x01the \x05\x41water room\x05\x40 is open!\x09"),
    (0x9053, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43water room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! A \x05\x43chest\x05\x40\x01has appeared!\x09"),
    # 0x9054 and 0x9055 unused
    (0x9056, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44lobby and adult side\x05\x40\x01of the \x05\x46Spirit Temple\x05\x40! A \x05\x44chest\x05\x40 has\x01appeared!\x09"),
    # 0x9057 unused
    (0x9058, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43climbable wall\x05\x40 in the\x01\x05\x46Spirit Temple\x05\x40! The way to the\x01\x05\x43upstairs\x05\x40 is open!\x09"),
    # 0x9059 and 0x905A unused
    (0x905B, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41Fire Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40! The way to the \x05\x41final room\x05\x40 is\x01open!\x09"),
    (0x905C, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x45Shadow Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40! The way to the \x05\x45final\x01room\x05\x40 is open!\x09"),
    (0x905D, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43Water Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40! The way to the \x05\x43final\x01room\x05\x40 is open!\x09"),
    # 0x905E unused
    # Silver Rupee messages for non-MQ dungeons when all have been collected. Offset 0x44 from the base messages.
    # 0x905F unused
    (0x9060, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44spinning scythe room\x05\x40\x01in the \x05\x44Ice Cavern\x05\x40! The way to the\x01\x05\x44map room\x05\x40 is open!\x09"),
    (0x9061, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43push block room\x05\x40 in\x01the \x05\x44Ice Cavern\x05\x40! The way to the \x05\x43final\x01room\x05\x40 is open!\x09"),
    (0x9062, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the basement in the\x01\x05\x45Bottom of the Well\x05\x40! Now you can\x01get back to the upper level!\x09"),
    (0x9063, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42scythe shortcut room\x05\x40\x01in the \x05\x45Shadow Temple\x05\x40! Now you can\x01access the \x05\x42chest\x05\x40 there!\x09"),
    # 0x9064 unused
    (0x9065, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46huge pit\x05\x40 in the\x01\x05\x45Shadow Temple\x05\x40! The way to the\x01room with \x05\x46falling spikes\x05\x40 is open!\x09"),
    (0x9066, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the room with \x05\x45invisible\x01spikes\x05\x40 in the \x05\x45Shadow Temple\x05\x40! The\x01way to the room with the \x05\x45giant pot\x05\x40\x04is open!\x09"),
    (0x9067, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46sloped room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! The way to\x01the room with the \x05\x46heavy block\x05\x40 is\x04open!\x09"),
    (0x9068, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41lava room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! The way to\x01the \x05\x41water room\x05\x40 is open!\x09"),
    (0x9069, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x43water room\x05\x40 in the\x01\x05\x46Gerudo Training Ground\x05\x40! A \x05\x43chest\x05\x40\x01has appeared!\x09"),
    (0x906A, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41torch room\x05\x40 in the\x01child side of the \x05\x46Spirit Temple\x05\x40! Now\x01the \x05\x41metal bridge\x05\x40 there is lowered!\x09"),
    (0x906B, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42boulder room\x05\x40 in the\x01adult side of the \x05\x46Spirit Temple\x05\x40! Now\x01you can access the \x05\x42chest\x05\x40 there!\x09"),
    # 0x906C unused
    (0x906D, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46sun block room\x05\x40 in the\x01\x05\x46Spirit Temple\x05\x40! The \x05\x46torch\x05\x40 has been\x01lit!\x09"),
    # 0x906E unused
    (0x906F, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x46Spirit Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40! The way to the \x05\x46second room\x05\x40\x01is open!\x09"),
    (0x9070, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x44Light Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40! The way to the \x05\x44final room\x05\x40 is\x01open!\x09"),
    (0x9071, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x41Fire Trial\x05\x40 in \x05\x41Ganon's\x01Castle\x05\x40! The way to the \x05\x41final room\x05\x40 is\x01open!\x09"),
    # 0x9072 and 0x9073 unused
    (0x9074, "\x08You have found all of the \x05\x44Silver\x01Rupees\x05\x40 for the \x05\x42Forest Trial\x05\x40 in\x01\x05\x41Ganon's Castle\x05\x40! The way to the \x05\x42final\x01room\x05\x40 is open!\x09"),
    # Silver Rupee messages without count. Offset 0x5A from the base messages.
    (0x9075, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01staircase room in \x05\x41Dodongo's Cavern\x05\x40!\x09"),
    (0x9076, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44spinning scythe room\x05\x40 in the \x05\x44Ice\x01Cavern\x05\x40!\x09"),
    (0x9077, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43push block room\x05\x40 in the \x05\x44Ice Cavern\x05\x40!\x09"),
    (0x9078, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01basement in the \x05\x45Bottom of the Well\x05\x40!\x09"),
    (0x9079, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42scythe shortcut room\x05\x40 in the \x05\x45Shadow\x01Temple\x05\x40!\x09"),
    (0x907A, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44invisible blade room\x05\x40 in the \x05\x45Shadow\x01Temple\x05\x40!\x09"),
    (0x907B, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46huge pit\x05\x40 in the \x05\x45Shadow Temple\x05\x40!\x09"),
    (0x907C, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01room with \x05\x45invisible spikes\x05\x40 in the\x01\x05\x45Shadow Temple\x05\x40!\x09"),
    (0x907D, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46sloped room\x05\x40 in the \x05\x46Gerudo Training\x01Ground\x05\x40!\x09"),
    (0x907E, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x41lava\x01room\x05\x40 in the \x05\x46Gerudo Training Ground\x05\x40!\x09"),
    (0x907F, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43water room\x05\x40 in the \x05\x46Gerudo Training\x01Ground\x05\x40!\x09"),
    (0x9080, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x41torch room\x05\x40 in the child side of the\x01\x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9081, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42boulder room\x05\x40 in the adult side of the\x01\x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9082, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44lobby and adult side\x05\x40 of the \x05\x46Spirit\x01Temple\x05\x40!\x09"),
    (0x9083, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x46sun\x01block room\x05\x40 in the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9084, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43climbable wall\x05\x40 in the \x05\x46Spirit Temple\x05\x40!\x09"),
    (0x9085, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x46Spirit Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9086, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x44Light Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9087, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the \x05\x41Fire\x01Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9088, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x45Shadow Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x9089, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x43Water Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
    (0x908A, "\x08You found a \x05\x44Silver Rupee\x05\x40 for the\x01\x05\x42Forest Trial\x05\x40 in \x05\x41Ganon's Castle\x05\x40!\x09"),
]

dungeon_names = [
    None, # Unused Deku Tree
    None, # Unused Dodongos Cavern
    None, # Unused Jabu
    "the \x05\x42Forest Temple\x05\x40",
    "the \x05\x41Fire Temple\x05\x40",
    "the \x05\x43Water Temple\x05\x40",
    "the \x05\x46Spirit Temple\x05\x40",
    "the \x05\x45Shadow Temple\x05\x40",
    "the \x05\x45Bottom of the Well\x05\x40",
    None, # Unused Ice Cavern
    None, # Unused Ganons Castle Tower
    "the \x05\x46Gerudo Training\x01Ground\x05\x40",
    "the \x05\x46Thieves' Hideout\x05\x40",
    "\x05\x41Ganon's Castle\x05\x40",
    None, # Unused Tower Collapse
    None, # Unused Castle Collapse
    "the \x05\x44Treasure Box Shop\x05\x40",
]

i = 0x9101
# Add small key messages starting at 0x9101
# These are grouped in dungeon order as follows:
#       0x9101 - Small key messages for the first one collected
#       0x9112 - Small key messages containing the count
#       0x9123 - Small key messages for collecting more than enough

KEYSANITY_MESSAGE_TEMPLATES=[
    "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01It's your \x05\x41first\x05\x40 one!\x09",
    "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01You've collected \x05\x41\xF1{count}\x05\x40 of them.\x09",
    "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01You already have enough keys.\x09",
    "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for {dungeon_name}!\x09",
    "\x13\x77\x08You found a \x05\x41Key Ring\x05\x40\x01for {dungeon_name}!\x09\x01It includes the \x05\x41Boss Key\x05\x40!"
    ]
for dungeon_name in dungeon_names:
    if dungeon_name is not None:
        KEYSANITY_MESSAGES.append((i, f"\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01It's your \x05\x41first\x05\x40 one!\x09"))
    i += 1
c = 0
for dungeon_name in dungeon_names:
    if dungeon_name is not None:
        KEYSANITY_MESSAGES.append((i, f"\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01You've collected \x05\x41" + "\xF1" + c.to_bytes(1, 'big').decode() + "\x05\x40 of them.\x09"))
    i += 1
    c += 1
for dungeon_name in dungeon_names:
    if dungeon_name is not None:
        KEYSANITY_MESSAGES.append((i, f"\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for {dungeon_name}!\x01You already have enough keys.\x09"))
    i += 1

# Add key ring messages starting at 0x9200
i = 0x9200
for dungeon_name in dungeon_names:
    if dungeon_name is not None:
        KEYSANITY_MESSAGES.append((i, f"\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for {dungeon_name}!\x09"))
    i += 1

key_rings_with_bk_dungeon_names = [
    "the \x05\x42Forest Temple\x05\x40",
    "the \x05\x41Fire Temple\x05\x40",
    "the \x05\x43Water Temple\x05\x40",
    "the \x05\x46Spirit Temple\x05\x40",
    "the \x05\x45Shadow Temple\x05\x40"
]
for dungeon_name in key_rings_with_bk_dungeon_names:
    KEYSANITY_MESSAGES.append((i, f"\x13\x77\x08You found a \x05\x41Key Ring\x05\x40\x01for {dungeon_name}!\x09\x01It includes the \x05\x41Boss Key\x05\x40!"))
    i += 1

MISC_MESSAGES: list[tuple[int, tuple[str | bytearray, int]]] = [
    (0x0032, ("\x08\x13\x02You got \x05\x41Bombs\x05\x40!\x01If you see something\x01suspicious, bomb it!", 0x23)),
    (0x0033, ("\x08\x13\x09You got \x05\x41Bombchus\x05\x40!", 0x23)),
    (0x0034, ("\x08\x13\x01You got a \x05\x41Deku Nut\x05\x40!", 0x23)),
    (0x0037, ("\x08\x13\x00You got a \x05\x41Deku Stick\x05\x40!", 0x23)),
    (0x003B, ("\x08You cast Farore's Wind!\x01\x1C\x05\x42Return to \xF3\x01Dispel the Warp Point\x01Exit\x05\x40", 0x23)),
    (0x0043, ("\x08\x13\x15You got a \x05\x41Red Potion\x05\x40!\x01It will restore your health", 0x23)),
    (0x0044, ("\x08\x13\x16You got a \x05\x42Green Potion\x05\x40!\x01It will restore your magic.", 0x23)),
    (0x0045, ("\x08\x13\x17You got a \x05\x43Blue Potion\x05\x40!\x01It will recover your health\x01and magic.", 0x23)),
    (0x0046, ("\x08\x13\x18You caught a \x05\x41Fairy\x05\x40 in a bottle!\x01It will revive you\x01the moment you run out of life \x01energy.", 0x23)),
    (0x0047, ("\x08\x13\x19You got a \x05\x41Fish\x05\x40!\x01It looks so fresh and\x01delicious!", 0x23)),
    (0x004C, ("\x08\x13\x3EYou got a \x05\x44Deku Shield\x05\x40!", 0x23)),
    (0x004D, ("\x08\x13\x3FYou got a \x05\x44Hylian Shield\x05\x40!", 0x23)),
    (0x0050, ("\x08\x13\x42You got a \x05\x41Goron Tunic\x05\x40!\x01Going to a hot place? No worry!", 0x23)),
    (0x0051, ("\x08\x13\x43You got a \x05\x43Zora Tunic\x05\x40!\x01Wear it, and you won't drown\x01underwater.", 0x23)),
    (0x0055, ("\x08You got a \x05\x45Recovery Heart\x05\x40!\x01Your life energy is recovered!", 0x23)),
    (0x005D, ("\x08\x13\x1CYou put a \x05\x44Blue Fire\x05\x40\x01into the bottle!\x01This is a cool flame you can\x01use on red ice.", 0x23)),
    (0x007A, ("\x08\x13\x1DYou put a \x05\x41Bug \x05\x40in the bottle!\x01This kind of bug prefers to\x01live in small holes in the ground.", 0x23)),
    (0x0097, ("\x08\x13\x20You caught a \x05\x41Poe \x05\x40in a bottle!\x01Something good might happen!", 0x23)),
    (0x00DC, ("\x08\x13\x58You got \x05\x41Deku Seeds\x05\x40!\x01Use these as bullets\x01for your Slingshot.", 0x23)),
    (0x00E6, ("\x08You got a \x05\x46bundle of arrows\x05\x40!", 0x23)),
    (0x00F9, ("\x08\x13\x1EYou put a \x05\x41Big Poe \x05\x40in a bottle!\x01Let's sell it at the \x05\x41Ghost Shop\x05\x40!\x01Something good might happen!", 0x23)),
    (0x507B, (list(bytearray(
            b"\x08I tell you, I saw him!\x04"
            b"\x08I saw the ghostly figure of Damp\x96\x01"
            b"the gravekeeper sinking into\x01"
            b"his grave. It looked like he was\x01"
            b"holding some kind of \x05\x41treasure\x05\x40!\x02"
            )), 0x00)),
    (0x0422, ("They say that once \x05\x41Morpha's Curse\x05\x40\x01is lifted, striking \x05\x42this stone\x05\x40 can\x01shift the tides of \x05\x44Lake Hylia\x05\x40.\x02", 0x23)),
    (0x401C, ("Please find my dear \05\x41Princess Ruto\x05\x40\x01immediately... Zora!\x12\x68\x7A", 0x03)),
    (0x9100, ("I am out of goods now.\x01Sorry!\x04The mark that will lead you to\x01the Spirit Temple is the \x05\x41flag on\x01the left \x05\x40outside the shop.\x01Be seeing you!\x02", 0x00)),
    (0x0451, ("\x12\x68\x7AMweep\x07\x04\x52", 0x23)),
    (0x0452, ("\x12\x68\x7AMweep\x07\x04\x53", 0x23)),
    (0x0453, ("\x12\x68\x7AMweep\x07\x04\x54", 0x23)),
    (0x0454, ("\x12\x68\x7AMweep\x07\x04\x55", 0x23)),
    (0x0455, ("\x12\x68\x7AMweep\x07\x04\x56", 0x23)),
    (0x0456, ("\x12\x68\x7AMweep\x07\x04\x57", 0x23)),
    (0x0457, ("\x12\x68\x7AMweep\x07\x04\x58", 0x23)),
    (0x0458, ("\x12\x68\x7AMweep\x07\x04\x59", 0x23)),
    (0x0459, ("\x12\x68\x7AMweep\x07\x04\x5A", 0x23)),
    (0x045A, ("\x12\x68\x7AMweep\x07\x04\x5B", 0x23)),
    (0x045B, ("\x12\x68\x7AMweep", 0x23)),
    (0x045C, ("Come back when you have\x01your own bow and you'll get the\x01\x05\x41real prize\x05\x40!\x0E\x78", 0x00)),
    (0x045D, ("\x12\x68\x5F\x05\x44This game seems shady. Maybe\x01the \x05\x41eye of truth\x05\x44 will show the\x01way forward?\x0E\x78", 0x00)),
    (0x6013, ("Hey, newcomer!\x04Want me to throw you in jail?\x01\x01\x1B\x05\x42No\x01Yes\x05\x40", 0x00)),
]

PATCH_TEXTS = {
    "wow": "{world_id} of {world_count}",
    "ordinary": "ordinary",
    "masterful": "masterful",
    "claim": "Brrrring me the Claim Check...\x01to rrreceive anotherrrrrr item...",
    "brought_poe": "\x1AOh, you brought a Poe today!\x04\x1AHmmmm!\x04\x1AVery interesting!\x01This is a \x05\x41Big Poe\x05\x40!\x04\x1AI'll buy it for \x05\x4150 Rupees\x05\x40.\x04On top of that, I'll put \x05\x41100\x01points \x05\x40on your card.\x04\x1AIf you earn \x05\x41{poe} points\x05\x40, you'll\x01be a happy man! Heh heh.",
    "enough_poe": "\x1AWait a minute! WOW!\x04\x1AYou have earned \x05\x41{poe} points\x05\x40!\x04\x1AYoung man, you are a genuine\x01\x05\x41Ghost Hunter\x05\x40!\x04\x1AIs that what you expected me to\x01say? Heh heh heh!\x04\x1ABecause of you, I have extra\x01inventory of \x05\x41Big Poes\x05\x40, so this will\x01be the last time I can buy a \x01ghost.\x04\x1AYou're thinking about what I \x01promised would happen when you\x01earned {poe} points. Heh heh.\x04\x1ADon't worry, I didn't forget.\x01Just take this.",
    "child_anju": "\x08What should I do!?\x01My \x05\x41Cuccos\x05\x40 have all flown away!\x04You, little boy, please!\x01Please gather at least \x05\x41{chicken} Cuccos\x05\x40\x01for me.\x02",
    "ruto_nothing": "\x08Princess Ruto got \x01\x05\x43nothing\x05\x40!\x01Well, that's disappointing...\x02",
    "ruto_fool": "\x08Princess Ruto is a \x05\x43FOOL\x05\x40!\x01But why Princess Ruto?\x02",
    "ruto_text": "\x08Princess Ruto got \x01\x05{color}{reward_text}\x05\x40!\x01But why Princess Ruto?\x02",
    "gallop": "Hey newcomer, you have a fine \x01horse!\x04I don't know where you stole \x01it from, but...\x04OK, how about challenging this \x01\x05\x41horseback archery\x05\x40?\x04Once the horse starts galloping,\x01shoot the targets with your\x01arrows. \x04Let's see how many points you \x01can score. You get 20 arrows.\x04If you can score \x05\x411,000 points\x05\x40, I will \x01give you something good! And even \x01more if you score \x05\x411,500 points\x05\x40!\x0B\x02",
    "bombchu_desc": '\x08\x05\x41Bombchu   (5 pieces)   60 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it\'s actually a self-propelled time\x01bomb!\x09\x0A',
    "bombchu_purc": '\x08Bombchu    5 Pieces    60 Rupees\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x09',
    "bombchu_desc_10": "\x08\x05\x41Bombchu  (10 pieces)  99 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it's actually a self-propelled time\x01bomb!\x09\x0A",
    "bombchu_purc_10": "\x08Bombchu  10 pieces   99 Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40",
    "blue_potion_desc": "\x08\x05\x43Blue Potion 100 Rupees\x01\x05\x40If you drink this, you will\x01recover your life energy and magic.\x09\x0A",
    "blue_potion_purc": "\x08Blue Potion 100 Rupees\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40",
    "scrub_text": "\x08All right! You win! In return,\x01I will sell you {item}!\x01\x05\x41{price} Rupees \x05\x40it is!",
    "mysterious": "mysterious item",
    "bean_mysterious": "\x1AChomp chomp chomp...\x01We have... \x05\x41a mysterious item\x05\x40! \x01Do you want it...huh? Huh?\x04\x05\x41\x0860 Rupees\x05\x40 and it's yours!\x01Keyahahah!\x01\x1B\x05\x42Yes\x01No\x05\x40\x02",
    "bean_wrapped": "\x1AChomp chomp chomp...We have...\x01\x05\x41{item}\x05\x40!\x04\x05\x41\x0860 Rupees\x05\x40 and it's yours!\x01Keyahahah!\x01\x1B\x05\x42Yes\x01No\x05\x40\x02",
    "bean_item": "\x1AChomp chomp chomp...We have...\x01\x05\x41{item}\x05\x40! \x01Do you want it...huh? Huh?\x04\x05\x41\x0860 Rupees\x05\x40 and it's yours!\x01Keyahahah!\x01\x1B\x05\x42Yes\x01No\x05\x40\x02",
    "bean_low": "You don't have enough money.\x01I can't sell it to you.\x01Chomp chomp...\x02",
    "bean_enough": "We hope you like it!\x01Chomp chomp chomp.\x02",
    "carpet_mysterious": "\x06\x41Well Come!\x04I am selling stuff, strange and \x01rare, from all over the world to \x01everybody.\x01Today's special is...\x04A mysterious item! \x01Intriguing! \x01I won't tell you what it is until \x01I see the money....\x04How about \x05\x41200 Rupees\x05\x40?\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "carpet_wrapped": "\x06\x41Well Come!\x04I am selling stuff, strange and \x01rare. Today's special is...\x01\x05\x41{item}\x05\x40!\x04How about \x05\x41200 Rupees\x05\x40?\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "carpet_item": "\x06\x41Well Come!\x04I am selling stuff, strange and \x01rare, from all over the world to \x01everybody. Today's special is...\x01\x05\x41{item}\x05\x40! \x01\x04How about \x05\x41200 Rupees\x05\x40?\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "carpet_enough": "Thank you very much!\x04The mark that will lead you to\x01the Spirit Temple is the \x05\x41flag on\x01the left \x05\x40outside the shop.\x01Be seeing you!\x02",
    "medigoron_cool": "I have something cool right here.\x01How about it...\x07\x30\x4F\x02",
    "medigoron_ask": "How do you like it?\x02",
    "medigoron_mysterious": "How about buying this cool item for \x01200 Rupees?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "medigoron_wrapped": "For 200 Rupees, how about buying...\x04\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "medigoron_item": "For 200 Rupees, how about buying \x01\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "granny_mysterious": "Mysterious item! How about\x01\x05\x41100 Rupees\x05\x40?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "granny_wrapped": "How about \x05\x41100 Rupees\x05\x40 for...\x04\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "granny_item": "How about \x05\x41100 Rupees\x05\x40 for\x01\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02",
    "play": "All right. You don't have to play\x01if you don't want to.\x0B\x02",
    "salesman_mysterious": "I seem to have misplaced my\x01keys, but I have a fun item to\x01sell instead.\x04How about \x05\x4110 Rupees\x05\x40?\x01\x01\x1B\x05\x42Buy\x01Don't Buy\x05\x40\x02",
    "salesman_wrapped": "I seem to have misplaced my\x01keys, but I have a fun item to\x01sell instead.\x01How about \x05\x4110 Rupees\x05\x40 for...\x04\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't Buy\x05\x40\x02",
    "salesman_item": "I seem to have misplaced my\x01keys, but I have a fun item to\x01sell instead.\x04How about \x05\x4110 Rupees\x05\x40 for\x01\x05\x41{item}\x05\x40?\x01\x1B\x05\x42Buy\x01Don't Buy\x05\x40\x02",
    "ok": "That's OK!\x01More fun for me.\x0B\x02",
    "limit": "Wait, that room was off limits!\x02",
    "hope": "I hope you like it!\x02",
    "map": "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the {dungeon_name}\x05\x40!\x01It\'s {dungeon_state}!\x09",
    "compass_rando": "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the {dungeon_name}\x05\x40!\x01The {vanilla_reward} can be found\x01{area}!\x09",
    "compass": "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the {dungeon_name}\x05\x40!\x01It holds the \x05{color}{dungeon_reward}\x05\x40!\x09",
    "tycoon": "\x08\x13\x57You got a \x05\x43Tycoon's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46999\x05\x40 \x05\x46Rupees\x05\x40.",
    "blue_fire_arrow": "\x08\x13\x0CYou got the \x05\x43Blue Fire Arrow\x05\x40!\x01This is a cool arrow you can\x01use on red ice.",
    "censor": ['cum', 'cunt', 'dike', 'penis', 'puss', 'rape', 'shit'],
    "shop_dungeon_desc_multi": '\x08\x05\x41{base_name}  {price} Rupees\x01({extra_name})\x01\x05\x42Player {player_id}\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02',
    "shop_dungeon_desc": '\x08\x05\x41{base_name}  {price} Rupees\x01({extra_name})\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02',
    "shop_dungeon_purc": '\x08{base_name}  {price} Rupees\x09\x01({extra_name})\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02',
    "shop_desc_multi": '\x08\x05\x41{base_name}  {price} Rupees\x01\x05\x42Player {player_id}\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02',
    "shop_desc": '\x08\x05\x41{base_name}  {price} Rupees\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02',
    "shop_perc": '\x08{base_name} {price} Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02'
}
# prefix_n=patch["o_the_1"]+" " if dungeon.name not in ('Dodongos Cavern', 'Jabu Jabus Belly') else ""

dungeon_list = {
    #                      dungeon name                      compass map gender
    'Deku Tree':          ("the \x05\x42Deku Tree",          0x62, 0x88, "o"),
    'Dodongos Cavern':    ("\x05\x41Dodongo\'s Cavern",      0x63, 0x89, "o"),
    'Jabu Jabus Belly':   ("\x05\x43Jabu Jabu\'s Belly",     0x64, 0x8a, "o"),
    'Forest Temple':      ("the \x05\x42Forest Temple",      0x65, 0x8b, "o"),
    'Fire Temple':        ("the \x05\x41Fire Temple",        0x7c, 0x8c, "o"),
    'Water Temple':       ("the \x05\x43Water Temple",       0x7d, 0x8e, "o"),
    'Spirit Temple':      ("the \x05\x46Spirit Temple",      0x7e, 0x8f, "o"),
    'Ice Cavern':         ("the \x05\x44Ice Cavern",         0x87, 0x92, "o"),
    'Bottom of the Well': ("the \x05\x45Bottom of the Well", 0xa2, 0xa5, "o"),
    'Shadow Temple':      ("the \x05\x45Shadow Temple",      0x7f, 0xa3, "o"),
}

prefix = {
    "gender":["o"],
    "prefix":{
        "vowel": ["a","e","i","o","u"],
        "definite":{
            "*":"the"
            },
        "indefinite":{
            "vowel":"an",
            "*":"a"
        }
    }
}

PLANE_TEXTS = {}

d = {
    'prefix': prefix,
    'dungeon_list': dungeon_list,
    'ITEM_MESSAGES': ITEM_MESSAGES,
    'dungeon_names': dungeon_names,
    'key_rings_with_bk_dungeon_names': key_rings_with_bk_dungeon_names,
    'KEYSANITY_MESSAGE_TEMPLATES': KEYSANITY_MESSAGE_TEMPLATES,
    'MISC_MESSAGES': MISC_MESSAGES,
    "PATCH_TEXTS": PATCH_TEXTS,
    "PLANE_TEXTS": PLANE_TEXTS,
}
json.dump(d,open("./en_message.otrx",mode="w+"), ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))