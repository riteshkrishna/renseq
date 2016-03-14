quantile(breadth, [.25, .5, .75, .95])

quantile(readcount, [.25, .5, .75, .95])

mu_read = mean(readcount)
std_read = std(readcount)
readcount_norm = (readcount - mu_read)/std_read
readcount_range = (readcount - min(readcount))/(max(readcount) - min(readcount))

figure;
scatter(readcount_range, breadth)

% Create a combined measure of range and breadth both
combined_measure = readcount_range .* breadth

figure; 
histogram(combined_measure)

% Decide on a threshold
Q = quantile(combined_measure,[.25 .5 .75 .95])
[sorted_combinedmeasure, sorted_idx] = sort(combined_measure);

figure;
plot(sorted_combinedmeasure)

filtered_idx = find(sorted_combinedmeasure > Q(3))

filtered_readcount = readcount_range(sorted_idx(filtered_idx));
filtered_breadth = breadth(sorted_idx(filtered_idx));
filtered_chrnames = chr(sorted_idx(filtered_idx));
filtered_start = loc_start(sorted_idx(filtered_idx));
filtered_end = loc_end(sorted_idx(filtered_idx));
F = [filtered_start filtered_end filtered_readcount filtered_breadth];

figure;
scatter(filtered_readcount,filtered_breadth)

figure;
histogram(filtered_readcount)

figure;
histogram(filtered_breadth)

% print some names from end
total_filtered = size(filtered_chrnames,1)
for i=total_filtered-20:total_filtered
    sprintf('%s:%d..%d \t%f \t%f',filtered_chrnames{i},F(i,1), F(i,2),F(i,3), F(i,4))
end




