% for query in root.queries:
%   for selection in query.selection:
${selection.name}:${selection.type}
%   endfor
% endfor
