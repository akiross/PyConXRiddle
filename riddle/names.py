import random


# Using list(set()) to avoid duplicates and allow indexing
_adjectives = list(set('''
admiring adoring affectionate agitated amazing angry awesome blissful boring
brave clever cocky compassionate competent condescending confident cranky
dazzling determined distracted dreamy eager ecstatic elastic elated elegant
eloquent epic fervent festive flamboyant focused friendly frosty gallant gifted
goofy gracious happy hardcore heuristic hopeful hungry infallible inspiring
jolly jovial keen kind laughing loving lucid mystifying modest musing naughty
nervous nifty nostalgic objective optimistic peaceful pedantic pensive
practical priceless quirky quizzical relaxed reverent romantic sad serene
sharp silly sleepy stoic stupefied suspicious tender thirsty trusting unruffled
upbeat vibrant vigilant vigorous wizardly wonderful xenodochial youthful
zealous zen
'''.split()))


_names = list(set('''
albattani allen almeida agnesi archimedes ardinghelli aryabhata austin babbage
banach bardeen bartik bassi beaver bell benz bhabha bhaskara blackwell bohr
booth borg bose boyd brahmagupta brattain brown carson chandrasekhar shannon
clarke colden cori cray curran curie darwin davinci dijkstra dubinsky easley
edison einstein elion engelbart euclid euler fermat fermi feynman franklin
galileo gates goldberg goldstine goldwasser golick goodall haibt hamilton
hawking heisenberg hermann heyrovsky hodgkin hoover hopper hugle hypatia
jackson jang jennings jepsen johnson joliot jones kalam kare keller kepler
khorana kilby kirch knuth kowalevski lalande lamarr lamport leakey leavitt
lewin lichterman liskov lovelace lumiere mahavira mayer mccarthy mcclintock
mclean mcnulty meitner meninsky mestorf minsky mirzakhani morse murdock neumann
newton nightingale nobel noether northcutt noyce panini pare pasteur payne
perlman pike poincare poitras ptolemy raman ramanujan ride montalcini ritchie
roentgen rosalind saha sammet shaw shirley shockley sinoussi snyder spence
stallman stonebraker swanson swartz swirles tesla thompson torvalds turing
varahamihira visvesvaraya volhard wescoff wiles williams wilson wing wozniak
wright yalow yonath pythagoras weierstrass alexander
'''.split()))


_animals = list(set('''
aardvark albatross alligator alpaca ant anteater antelope ape armadillo baboon
badger barracuda bat bear beaver bee bird bison boar buffalo butterfly camel
caribou cassowary cat caterpillar chameleon chamois cheetah chicken chimpanzee
chinchilla chough coati cobra cockroack cod cormorant coyote crab crane
crocodile crow curlew deer dinosaur dog dolphin donkey dotterel dove dragon
dragonfly duck dugong dunlin eagle echidna eel eland elephant elk emu falcon
ferret finch fish flamingo fly fox frog gaur gazelle gerbil giraffe gnat gnu
goat goldfinch goldfish goosander goshawk grasshopper grouse guanaco gull
hamster hare hawk hedgehog heron herring hippo hornet horse hummingbird hyena
ibex ibis impala jackal jaguar jay jellyfish kangaroo kinkajou koala kouprey
kudu lapwing lark lemur leopard lion llama lobster locust loris louse lyrebird
magpie mallard mammoth manatee mandrill mink mole mongoose monkey moose
mosquito mouse narwhal newt nightingale octopus okapi opossum ostrich otter
owl oyster panther parrot panda partridge pelican penguin pheasant pidgeon
pony porcupine porpoise pug quail quelea quetzal rabbit raccoon ram rat raven
reindeer rhinoceros rook salamander salmon sandpiper sardine seahorse seal
shark sheep shrew siamang skunk sloth snail snake spider squid squirrel
starling stegoraurus swan tapir tarsier termite tiger toad tortoise turkey
turtle wallaby walrus wasp weasel whale wolf wolverine wombat wren yak zebra
'''.split()))


def random_name(sep='_'):
    first = random.choice(_names)
    second = random.choice(_adjectives)
    return f"{first}{sep}{second}"


def random_animal(sep='_'):
    first = random.choice(_names)
    second = random.choice(_adjectives)
    third = random.choice(_animals)
    return f"{first}{sep}the{sep}{second}{sep}{third}"
