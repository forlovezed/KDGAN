% train1m - mirflick08 - assignment

MAP = [0.126 0.124 0.155 0.021 0.130; ...
0.207 0.205 0.177 0.092 0.217; ...
0.318 0.297 0.281 0.080 0.326; ...
0.558 0.556 0.538 0.274 0.568; ...
0.200 0.201 0.218 0.083 0.207; ...
0.520 0.518 0.410 0.323 0.530; ...
0.440 0.438 0.427 0.344 0.444; ...
0.278 0.279 0.304 0.232 0.282; ...
0.432 0.429 0.422 0.208 0.443; ...
0.535 0.536 0.511 0.467 0.537; ...
0.443 0.443 0.485 0.389 0.447; ...
0.077 0.075 0.073 0.035 0.079; ...
0.173 0.173 0.171 0.103 0.176; ...
0.397 0.397 0.346 0.168 0.405];

tags_name = {'baby', 'bird', 'car', 'cloud', 'dog', 'flower', 'girl', 'man', 'night', 'people', 'portrait', 'river', 'sea', 'tree'};
method_names = {'KNN', 'TagVote', 'RelExample', 'TagFeature', 'TagProp'};

[~, idx] = sort(MAP(:,5), 'descend');

figure('units', 'normalized', 'position', [.1 .1 .6 .3]);
plot_tags(tags_name(idx), method_names([1,2,5,4,3]), MAP(idx, 1), MAP(idx, 2), MAP(idx, 5), MAP(idx, 4), MAP(idx, 3));
xlim([0,0.6]);
saveTightFigure('mirflickr_train1m_MAP.pdf');