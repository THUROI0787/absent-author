# Batch size and the onset of overfitting

<!-- Synthetic fixture written for slop_lint.py tests: plain, specific, human-style prose. -->

We trained a 6-layer transformer on the character-level Shakespeare corpus with batch sizes of 32, 64 and 256, and stopped each run when validation loss had not improved for 2,000 steps. The smallest batch overfit first: its validation loss bottomed out at step 4,100, against 6,800 for the largest. We expected the opposite, because smaller batches inject more gradient noise and noise is usually described as a regulariser.

Two explanations fit this result. The first is that we held the learning rate fixed, so the small-batch runs took many more optimizer steps per epoch and simply saw the training set more often by the time we compared them. The second is that the noise scale at batch size 32 was already past the point where it helps. Re-plotting loss against epochs instead of steps removes most of the gap, which points to the first explanation; we did not test the second.

We used Adam with the default betas and a cosine schedule. Each configuration was run once, so differences smaller than about 0.02 nats are within the run-to-run spread we measured on a separate pair of repeated runs. The code and the exact configurations are in the accompanying repository, and the per-step logs are included so that the curves in Figure 2 can be regenerated.

This leaves a practical rule that we think is safe to state: when comparing batch sizes, compare at equal epochs, or scale the learning rate with the batch. Anything stronger would need more seeds and at least one other dataset.
