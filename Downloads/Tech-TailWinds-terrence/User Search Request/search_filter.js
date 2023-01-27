/* 
To go inside HTML Code under input div (optional): 

Put input inside tag-container:
<div class="tag-container">
    <input type="text" class="form-control" placeholder="Where do you want to go?">
</div>

*/
const tagContainer = document.querySelector('.tag-container');
const input = document.querySelector('.tag-container input');
var tags = [];

function createTag(label) {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    const removeButton = document.createElement('i');
    removeButton.setAttribute('class', 'material-icons');
    removeButton.setAttribute('item-data', label);
    removeButton.innerHTML = 'close';

    div.appendChild(span);
    div.appendChild(removeButton);
    return div;
}

// avoids repeating tags
function reset() {
    document.querySelectorAll('.tag').forEach(function(tag) {
        tag.parentElement.removeChild(tag);
    })
}

// adds new tags to array (adds them to front b/c prepend)
function addTags() {
    reset();
    tags.slice().reverse().forEach(function(tag) {
        const input = createTag(tag);
        tagContainer.prepend(input);
    })
}

// creates a new tag (and adds to tags) by pressing enter key
input.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
        tags.push(input.value);
        addTags();
        input.value = '';
    }
})

// remove button functionality w/ spread operator
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'I') {
        const value = e.target.getAttribute('item-data');
        const index = tags.indexOf(value);
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        addTags();
    }
})
