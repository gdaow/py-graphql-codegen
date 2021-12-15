<%def name="operation_type(node, suffix)">\
interface ${ (node.name + suffix) | camel} {
    % for it in node.selection:
        ${it.name}: ${it.type},
    % endfor
}
</%def>\
% for query in root.queries:
  ${operation_type(query, 'Query')}\
% endfor

% for mutation in root.mutations:
  ${operation_type(mutation, 'Mutation')}\
% endfor
