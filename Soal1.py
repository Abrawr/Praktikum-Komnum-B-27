import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Implementasi metode Regula Falsi untuk mencari akar fungsi
    
    Parameters:
    f (sympy expression): Fungsi yang akan dicari akarnya
    a (float): Batas bawah interval awal
    b (float): Batas atas interval awal
    tol (float): Toleransi error (default: 1e-6)
    max_iter (int): Maksimum iterasi (default: 100)
    
    Returns:
    tuple: (akar, tabel_iterasi, jumlah_iterasi)
    """
    # Konversi fungsi sympy ke fungsi numpy
    f_np = sp.lambdify(sp.symbols('x'), f, 'numpy')
    
    # Inisialisasi tabel iterasi
    tabel_iterasi = []
    
    # Cek apakah tanda fungsi di a dan b berlawanan
    fa = f_np(a)
    fb = f_np(b)
    
    if fa * fb > 0:
        raise ValueError("Fungsi harus memiliki tanda yang berbeda di a dan b")
    
    # Iterasi utama
    for iterasi in range(1, max_iter + 1):
        # Hitung titik c dengan metode regula falsi
        c = (a * fb - b * fa) / (fb - fa)
        fc = f_np(c)
        
        # Simpan data iterasi
        tabel_iterasi.append([iterasi, a, b, c, fa, fb, fc, abs(fc)])
        
        # Cek kriteria berhenti
        if abs(fc) < tol:
            break
            
        # Update interval
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    return c, tabel_iterasi, iterasi

def plot_fungsi(f, a, b, akar=None):
    """
    Plot fungsi dan titik akar jika ada
    
    Parameters:
    f (sympy expression): Fungsi yang akan diplot
    a (float): Batas bawah plot
    b (float): Batas atas plot
    akar (float): Titik akar yang akan ditandai (optional)
    """
    # Konversi fungsi sympy ke fungsi numpy
    f_np = sp.lambdify(sp.symbols('x'), f, 'numpy')
    
    # Buat data untuk plot
    x_vals = np.linspace(a, b, 400)
    y_vals = f_np(x_vals)
    
    # Buat plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f'f(x) = {str(f)}')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    
    # Tandai akar jika ada
    if akar is not None:
        plt.scatter([akar], [0], color='red', label=f'Akar ≈ {akar:.6f}')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Grafik Fungsi dan Pencarian Akar dengan Metode Regula Falsi')
    plt.legend()
    plt.show()

def main():
    # Input fungsi
    x = sp.symbols('x')
    fungsi_input = input("Masukkan fungsi f(x) (gunakan sintaks Python, contoh: x**2 - 2): ")
    try:
        f = sp.sympify(fungsi_input)
    except:
        print("Error: Fungsi tidak valid. Gunakan sintaks Python yang benar.")
        return
    
    # Input interval
    a = float(input("Masukkan batas bawah interval (a): "))
    b = float(input("Masukkan batas atas interval (b): "))
    
    # Jalankan metode Regula Falsi
    try:
        akar, tabel_iterasi, iterasi = regula_falsi(f, a, b)
        
        # Tampilkan hasil
        print("\nHasil:")
        print(f"Akar ditemukan di x ≈ {akar:.8f} setelah {iterasi} iterasi")
        
        # Tampilkan tabel iterasi
        print("\nTabel Iterasi:")
        print("Iterasi |     a     |     b     |     c     |    f(a)   |    f(b)   |    f(c)   |  Error")
        print("-" * 90)
        for row in tabel_iterasi:
            print(f"{row[0]:7d} | {row[1]:.6f} | {row[2]:.6f} | {row[3]:.6f} | {row[4]:.6f} | {row[5]:.6f} | {row[6]:.6f} | {row[7]:.6f}")
        
        # Plot fungsi
        plot_fungsi(f, a, b, akar)
        
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Program Metode Regula Falsi")
    print("---------------------------")
    main()