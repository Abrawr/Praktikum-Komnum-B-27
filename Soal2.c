#include <stdio.h>
#include <math.h>

#define MAX_ITER 10

// Fungsi yang ingin diintegrasikan
double f(double x) {
    return 4 * x * x * x; // Contoh: integral 4x^3 dari 0 sampai 1 = 1
}

// Metode Trapezoidal
double trapezoidal(double a, double b, int n) {
    double h = (b - a) / n;
    double sum = 0.5 * (f(a) + f(b));
    
    for (int i = 1; i < n; i++) {
        sum += f(a + i * h);
    }
    
    return h * sum;
}

// Integrasi Romberg dengan penjelasan
void romberg_integration(double a, double b, double eps) {
    double R[MAX_ITER][MAX_ITER];
    int i, j;

    printf("\n==============================================\n");
    printf("INTEGRASI ROMBERG: PENJELASAN LANGKAH DEMI LANGKAH\n");
    printf("==============================================\n\n");
    printf("Fungsi: ∫(4x^3) dx dari %g sampai %g\n", a, b);
    printf("Nilai eksak: 1.000000\n\n");

    // Langkah 1: Inisialisasi dengan Trapezoidal 1 interval
    R[0][0] = trapezoidal(a, b, 1);
    printf("LANGKAH 1: Metode Trapezoidal Dasar\n");
    printf("-> n=1 interval → Hasil = %.6f (Error: %.6f)\n\n", R[0][0], fabs(R[0][0] - 1));

    for (i = 1; i < MAX_ITER; i++) {
        // Langkah 2: Hitung trapezoidal dengan interval lebih halus
        int n_current = pow(2, i);
        R[i][0] = trapezoidal(a, b, n_current);
        
        printf("LANGKAH 2.%d: Trapezoidal dengan %d interval\n", i, n_current);
        printf("-> Hasil Trapezoidal = %.6f (Error: %.6f)\n", R[i][0], fabs(R[i][0] - 1));

        // Langkah 3: Ekstrapolasi Romberg
        printf("LANGKAH 3.%d: Ekstrapolasi Romberg\n", i);
        for (j = 1; j <= i; j++) {
            R[i][j] = R[i][j-1] + (R[i][j-1] - R[i-1][j-1]) / (pow(4, j) - 1);
            printf("   -> R[%d][%d] = %.6f (Error: %.6f)\n", 
                   i, j, R[i][j], fabs(R[i][j] - 1));
        }

        // Cek konvergensi
        if (i > 0 && fabs(R[i][i] - R[i-1][i-1]) < eps) {
            printf("\nKONVERGENSI DICAPAI!\n");
            printf("Hasil akhir Romberg: %.10f (Error: %.10f)\n", R[i][i], fabs(R[i][i] - 1));
            printf("Dibutuhkan %d iterasi dengan maksimal %d interval.\n", i, n_current);
            return;
        }
        printf("\n");
    }

    printf("Maksimum iterasi tercapai.\n");
    printf("Hasil terbaik: %.10f (Error: %.10f)\n", R[MAX_ITER-1][MAX_ITER-1], fabs(R[MAX_ITER-1][MAX_ITER-1] - 1));
}

int main() {
    double a = 0.0;   // Batas bawah
    double b = 1.0;   // Batas atas
    double eps = 1e-6; // Toleransi error

    romberg_integration(a, b, eps);

    // Bandingkan dengan trapezoidal murni
    printf("\n==============================================\n");
    printf("PERBANDINGAN DENGAN TRAPEZOIDAL MURNI\n");
    printf("==============================================\n");
    printf("Agar error < %g, metode Trapezoidal membutuhkan:\n", eps);
    for (int n = 1; n <= 1000000; n *= 2) {
        double result = trapezoidal(a, b, n);
        double error = fabs(result - 1);
        printf("-> n=%7d → Hasil=%.8f (Error=%.8f)\n", n, result, error);
        if (error < eps) break;
    }

    return 0;
}