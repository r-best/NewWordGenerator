# Word Generator

Using a dataset of phonetic representations of words in a given language, it should be possible to build a model that can generate new words that *sound* like the target language, but don't actually exist

Preliminarily using the [CMU Pronouncing Dictionary dataset](http://www.speech.cs.cmu.edu/cgi-bin/cmudict), subject to change

# Use
Run `script.py`, it will load the CMUDict dataset and allow you to start generating brand new words.

Words are generated in IPA format. If you, like me, don't know how to read IPA, Amazon's [Polly](https://eu-west-1.console.aws.amazon.com/polly/home/SynthesizeSpeech) service can generate speech from the symbols to let you hear what your new word sounds like, just switch to the SSML tab and enter the following tag:

```
<phoneme alphabet="ipa" ph="YOUR IPA TEXT HERE"></phoneme>
```

The [ARPAbet Wikipedia page]() also has a useful table of ARPAbet/IPA symbols to spoken sounds, so you can try to piece together the word yourself if Polly has trouble with it.