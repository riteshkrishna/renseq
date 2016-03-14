R = load('bed_info.mat')

% Decide on a threshold
min_base_threshold = 470;
base_satisfy_idx = R.basecovered > min_base_threshold;

figure;
histogram(R.breadth(base_satisfy_idx))

% Filter relevant data
readcount = R.readcount(base_satisfy_idx);
breadth = R.breadth(base_satisfy_idx);
length = R.length(base_satisfy_idx);
basecovered = R.basecovered(base_satisfy_idx);
chr = R.chr(base_satisfy_idx);
loc_start = R.loc_start(base_satisfy_idx);
loc_end = R.loc_end(base_satisfy_idx);

% Combined measure
readcount_range = (readcount - min(readcount))/(max(readcount) - min(readcount));
combined_measure = readcount_range .* breadth;

[sort_combine, sort_idx] = sort(combined_measure,'descend')

fid = fopen('Info.txt','w')
for i=1:size(sort_idx,1)
    index = sort_idx(i);
    fprintf(fid, '%s:%d..%d \t%d \t%f \t%d \t%d \n',chr{index},loc_start(index), loc_end(index),... 
            readcount(index), breadth(index), basecovered(index), length(index));
end

fclose(fid)
