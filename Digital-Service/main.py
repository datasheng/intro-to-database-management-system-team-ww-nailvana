from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='192.168.87.43', port=5000, debug=True, threaded=False)
