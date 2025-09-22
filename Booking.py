from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

SEAT_ROWS = ['A', 'B', 'C', 'D','E','F','G','H','I','J']
SEAT_COLS = ['1', '2', '3', '4', '5','6']

booked_seats_per_movie = {
    "Kung Fu Panda": [],
    "How To Train Your Dragon": [],
    "Angry Birds": [],
    "Ben 10": [],
    "Spider-Man": [],
    "Naruto": []
}

background_map = {
    "Kung Fu Panda": "movie1.jpg",
    "How To Train Your Dragon": "movie2.jpg",
    "Angry Birds": "movie3.jpg",
    "Ben 10": "movie4.jpg",
    "Spider-Man": "movie5.jpg",
    "Naruto": "movie6.jpg"
}

def generate_booking_id():
    return f"MCJA{random.randint(1000000000, 9999999999)}"

@app.route('/')
def select_movie():
    movies = ["Kung Fu Panda", "How To Train Your Dragon", "Angry Birds","Ben 10", "Spider-Man","Naruto"]
    return render_template("select_movie.html", movies=movies)

@app.route('/book/<movie>', methods=['GET', 'POST'])
def book(movie):
    if request.method == 'POST':
        if 'cancel_seat' in request.form:
            seat_to_cancel = request.form['cancel_seat']
            if seat_to_cancel in booked_seats_per_movie[movie]:
                booked_seats_per_movie[movie].remove(seat_to_cancel)
            return redirect(url_for('book', movie=movie))

        selected_seats = request.form.getlist("seat")
        for seat in selected_seats:
            if seat not in booked_seats_per_movie[movie]:
                booked_seats_per_movie[movie].append(seat)

        booking_id = generate_booking_id()
        return render_template("success_page.html",seats=selected_seats,movie=movie,booking_id=booking_id,background_image=background_map[movie])

    all_seats = []
    for row in SEAT_ROWS:
        for col in SEAT_COLS:
            all_seats.append(row + col)
    return render_template("index.html", seats=all_seats, booked=booked_seats_per_movie[movie], movie=movie)

if __name__ == '__main__':
    app.run(debug=True)