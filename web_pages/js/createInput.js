export default createInput

function createInput(section, id) {
    const label = document.createElement('label');
    label.for = id;
    label.textContent = id + ':';
    const input = document.createElement('input');
    input.type = 'text';
    input.id = id;
    input.name = id;
    input.required = true;

    section.append(label);
    section.append(input);

    return input;
}
