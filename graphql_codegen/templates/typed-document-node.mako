<%def name="operation_type(node)">\
interface ${node.name}Query {
    % for it in node.selection:
        ${it.name}: ${it.type},
    % endfor
}
</%def>\
% for operation in root.operations:
${operation_type(operation)}\
% endfor
