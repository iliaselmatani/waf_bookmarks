from flask import render_template, request, redirect, flash, url_for
from app import app, db
from app.models import Bookmark
from app.forms import PostBookmarkForm, EditBookmarkForm, DeleteBookmarkForm
from app.helpers import get_parameters, build_query, create_links
import datetime

@app.template_filter()
def datetimeformat(value, format='%Y-%m-%d'):
    return value.strftime(format)


@app.route('/', methods=['GET', 'POST'])
def index():
    # receive parameters from url query string
    params = get_parameters()

    # initialize forms:
    addform = PostBookmarkForm()
    editform = EditBookmarkForm()
    deleteform = DeleteBookmarkForm()
    
    # Add entry:
    if addform.validate() and "add" in request.form:
        new_bookmark = Bookmark(
                        url=addform.url.data, 
                        title=addform.title.data, 
                        description=addform.description.data,
                        date=datetime.datetime.utcnow()
                        )
        db.session.add(new_bookmark)
        db.session.commit()
        flash(f"Added: {new_bookmark.url}", 'success')
        return redirect(request.url)
    
    # Edit entry:
    if editform.validate() and "edit" in request.form:
        my_bookmark = Bookmark.query.filter_by(id=editform.myid.data).first()
        my_bookmark.url = editform.url.data
        my_bookmark.title = editform.title.data
        my_bookmark.description = editform.description.data
        db.session.commit()
        flash(f"Edited: {my_bookmark.url}", 'success')
        return redirect(request.url)
        
    # Delete entry:
    if deleteform.validate() and "delete" in request.form:
        my_bookmark = Bookmark.query.filter_by(id=deleteform.myid.data).first()
        db.session.delete(my_bookmark)
        db.session.commit()
        flash(f"Deleted: {my_bookmark.url}", 'danger')
        return redirect(request.url)

    # Build sql query:
    query = build_query(params)
    page = request.args.get('page', 1, type=int)
    paginate_query = query.paginate(page,5,False)

    # Build links
    links = create_links(query, params)

    # return links
 
    return render_template("index.html", data=paginate_query.items, addform=addform, 
                                         editform=editform, deleteform=deleteform, 
                                         links=links)

