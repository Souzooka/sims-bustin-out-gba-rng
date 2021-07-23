# sims-bustin-out-gba-rng
A recreation of the random number generation used by the GBA game Sims Bustin' Out.

Sims Bustin' Out uses a slightly modified implementation of a [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister), with a few variations. 
The most notable of which is that the implementation also has stateless RNG functions with their own incrementing index and that do not mutate the state of the rest of the MT.
