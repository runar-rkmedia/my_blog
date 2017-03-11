function edit_comment(comment_html_id, original_comment, comment_id) {
    var comment_body = document.getElementById("comment-id-body-" + comment_html_id);
    var comment_form = document.getElementById("comment-edit-form");
    var comment_text = document.getElementById("comment-text-" + comment_html_id);

    if (!document.body.contains(comment_form)) {
        comment_text.style.display = 'none';
        comment_body.innerHTML += `
    <form class="row add-comment-form" method="post" id="comment-edit-form">
        <label for="comment-input">Comment</label>
        <input type="hidden" name="blog_id" value="{{ blog_entry.key().id() }}">
        <input type="hidden" name="comment_id" value="` + comment_id + `">
        <textarea name="comment" class="twelve columns comment-input" id="comment-input">` + original_comment + `</textarea>
        <input class="three columns button-primary" type="submit" value="Post">
        <button type="button" class="three columns button-cancel" onclick="cancel_editing(` + comment_html_id + `)">Cancel</button>
        <input class="three columns button-dangerous u-pull-right" type="submit" value="Delete" name="delete_comment">
    </form>
    `;
    }
    return false;
}

function cancel_editing(comment_html_id) {
    var comment_form = document.getElementById("comment-edit-form");
    var comment_text = document.getElementById("comment-text-" + comment_html_id);
    comment_form.remove();
    comment_text.style.display = 'block';
}
