#!/bin/bash

echo "=== Combining datacards ==="
combineCards.py datacards/*.txt > combined_datacard.txt
echo "✓ Combined datacard created: combined_datacard.txt"

echo ""
echo "=== Creating workspace ==="
text2workspace.py combined_datacard.txt
echo "✓ Workspace created: workspace.root"

echo ""
echo "=== Running asymptotic limits (blind) ==="
combine -M AsymptoticLimits workspace.root -t -1 --expectSignal=0
echo "✓ Asymptotic limits completed"

#combine -M AsymptoticLimits workspace.root -t -1 --freezeParameters all --setParameters lumiscale=400.0/59.7
for cat in {1..15};
do
    echo ""
    echo "=== Running asymptotic limits for category $cat (blind) ==="
    text2workspace.py datacards/bs_tautau_${cat}_13TeV_.txt
    combine -M AsymptoticLimits datacards/bs_tautau_${cat}_13TeV_.root -t -1 --expectSignal=0 -n cat${cat}
    echo "✓ Asymptotic limits for category $cat completed"
done