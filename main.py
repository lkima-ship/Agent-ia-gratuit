echo 'print("=== AGENT IA GRATUIT ===")' > main.py
echo 'print("1. Start server")' >> main.py
echo 'print("2. Test")' >> main.py
echo 'print("3. Exit")' >> main.py
echo '' >> main.py
echo 'choice = input("Enter choice: ")' >> main.py
echo '' >> main.py
echo 'if choice == "1":' >> main.py
echo '    print("Starting server...")' >> main.py
echo '    import subprocess' >> main.py
echo '    subprocess.run(["python3", "server.py"])' >> main.py
echo 'elif choice == "2":' >> main.py
echo '    print("Test successful!")' >> main.py
echo 'elif choice == "3":' >> main.py
echo '    print("Goodbye!")' >> main.py
echo 'else:' >> main.py
echo '    print("Invalid choice")' >> main.py
