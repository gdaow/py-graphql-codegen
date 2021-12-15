<%def name="selection(items)">\
{
    % for it in items:
        %if it.is_scalar:
${it.name}: ${it.type}
        %elif it.is_object:
${it.name}: ${ selection(it.selection) | indent }
        %else:
...${it.name}
        %endif
    % endfor
}
</%def>

<%def name="operation(node, suffix)">
interface ${ (node.name + suffix) | camel} ${ local.selection(node.selection) | indent }
</%def>\

% for query in root.queries:
    ${operation(query, 'Query')}\
% endfor

% for mutation in root.mutations:
    ${operation(mutation, 'Mutation')}\
% endfor
