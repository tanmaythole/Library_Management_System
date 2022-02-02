from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request
from flask_login import login_required
from library.models import Members
from library import db
import math

members_ = Blueprint('members', __name__)

# Display Members
@members_.route('/members')
@login_required
def members():
    get_flashed_messages()
    rows_per_page = 15
    members = Members.query.all()

    length = len(members)

    last = math.ceil(length/rows_per_page)

    page = request.args.get('page')
    page = 1 if not str(page).isnumeric() else int(page)

    members = members[(page-1)*rows_per_page : page*rows_per_page]
    
    if page > 1:
        prev = '?page='+str(page-1)
    else:
        prev = '#'
    if page < last:
        next = '?page='+str(page+1)
    else:
        next = '#'

    pagination_msg = {
            "total":length, 
            "start":(page-1)*rows_per_page + 1, 
            "end": page*rows_per_page if page*rows_per_page < length else length
        }


    return render_template("members.html", members=members, prev=prev, next=next, pagination_msg=pagination_msg)

# Add/Edit Members
@members_.route('/members/add', methods=['GET', 'POST'])
@members_.route('/members/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def addMember(id=0):

    if id==0:
        params = {"isNew":True}
    else:
        params = Members.query.filter_by(id=id)[0]
    
    if request.method=='POST':
        if id==0:
            # add member
            try:
                r = request.form
                mem = Members(
                        name = r['name'],
                        email = r['email']
                    )
                db.session.add(mem)
                db.session.commit()
                flash(f"Member {mem.name} Added Successfully!!", "success")
                return redirect('/members')
            except Exception as e:
                flash(f'Something went wrong while adding the member - {e}', 'error')
                return render_template("addmember.html", params={params})
        else:
            # edit member of id
            try:
                r = request.form
                Members.query.filter_by(id=id).update(dict(name=r['name'], email=r['email']))
                db.session.commit()
                flash(f"Member {id} Updated Successfully!!", "success")
                return redirect('/members')
            except Exception as e:
                flash(f'Something went wrong while updating the member - {e}', 'error')
                return render_template("addmember.html", params={params})
                
    return render_template('addmember.html', params=params)

# Delete Member
@members_.route('/members/delete/<int:id>', methods=['DELETE', 'GET'])
@login_required
def deleteMember(id):
    try:
        mem = Members.query.filter_by(id=id).first()
        db.session.delete(mem)
        db.session.commit()
        flash(f"Member Deleted Successfully.", "success")
    except Exception as e:
        flash(f"Something Went Wrong - {e}", "error")
    return redirect('/members')
