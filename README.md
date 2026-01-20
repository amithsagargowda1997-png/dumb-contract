| Signal                     | Weight | Reason                |
| -------------------------- | ------ | --------------------- |
| Reentrancy flag            | +40    | High severity         |
| External call present      | +20    | Control transfer risk |
| Loop present               | +15    | Gas risk              |
| Loop + external call       | +30    | High gas-DoS risk     |
| Many public functions (>3) | +10    | Larger attack surface |
