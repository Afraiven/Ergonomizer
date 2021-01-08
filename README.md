# Ergonomizer
Project created for a competition

Ergonomizer to program mający na celu promocje ergonomii pracy przy komputerze,
zawiera on kilka przydatnych linków oraz funkcji pozwalających kontrolować naszą pozycję, częstotliwość mrugania oraz przypomina nam o rzeczach takich jak przerwy, ćwiczenia czy picie wody.
Jako iż przeważająca część społeczeństwa coraz częściej spędza długie godziny siedząc przed komputerem ważne jest aby wiedzieli że przestrzeganie kilku prostych zasad pomoże im zadbać o swoje zdrowie. Ergonomizer jest wszystkim czego potrzeba aby poznać oraz stosować się do tych zasad.

Po włączeniu programu ukazuje się okno startowe z informacją oraz możliwością zmiany języku.
Jest tak również przycisk 'Rozpocznij'  pozwalający przejść od drugiego okna, w którym można aktywować 3 funkcje, które oferuje program, jednakże przed włączeniem ich zalecane jest skalibrowanie kamery, wartości wykrywania mrugnięcia i wskazanie długości przekątnej ekranu w oknie 'Skalibruj'
Funkcje:
1. Mruganie - sprawdza częstotliwość mrugania korzystając z modułu pythona - 'dlib'.

2. Odległość - powiadamia użytkownika, kiedy ten zbliży się na odległość, która nie jest odpowiednia (odległość ta zależy od ustawionej w ekranie kalibracji przekątnej ekranu np. dla 15 cali to 40 cm dla 19 cali 60 cm itp.)

3. Przypominacz - służy on do przypominania od robieniu sobie przerw, aktywuje się co 15 minut.

Jeżeli funkcja 'Mruganie' bądz 'Odległość' będą włączone przez m.in. 10 minut ich kolor zmieni się na zielony oraz będzie możliwe utworzenie podsumowującego raportu używając przycisku 'Utwórz nowy raport'
