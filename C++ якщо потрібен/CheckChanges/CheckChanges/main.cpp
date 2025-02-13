#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <filesystem>
#include <unordered_map>
#include <list>
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace fs = std::filesystem;
namespace py = pybind11;

bool deleteFolder(const std::string& folderPath) {
    try {
        if (fs::exists(folderPath) && fs::is_directory(folderPath)) {
            fs::remove_all(folderPath);
            return true;
        }
        else {
            std::cerr << "����� �� ���� ��� �� �� �������: " << folderPath << std::endl;
            return false;
        }
    }
    catch (const fs::filesystem_error& e) {
        std::cerr << "������� ���������: " << e.what() << std::endl;
        return false;
    }
}

class SHA256 {
public:
    static std::string hash(const std::string& input);

private:
    static const size_t BLOCK_SIZE = 64;
    static const size_t OUTPUT_SIZE = 32;

    static const uint32_t k[64];
    static uint32_t rightRotate(uint32_t value, unsigned int count);
    static void processChunk(const uint8_t chunk[BLOCK_SIZE], uint32_t h[8]);
    static std::vector<uint8_t> padMessage(const std::string& message);
};

const uint32_t SHA256::k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

uint32_t SHA256::rightRotate(uint32_t value, unsigned int count) {
    return (value >> count) | (value << (32 - count));
}

void SHA256::processChunk(const uint8_t chunk[BLOCK_SIZE], uint32_t h[8]) {
    uint32_t w[64] = { 0 };
    for (int i = 0; i < 16; ++i) {
        w[i] = (chunk[i * 4] << 24) | (chunk[i * 4 + 1] << 16) |
            (chunk[i * 4 + 2] << 8) | chunk[i * 4 + 3];
    }
    for (int i = 16; i < 64; ++i) {
        uint32_t s0 = rightRotate(w[i - 15], 7) ^ rightRotate(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = rightRotate(w[i - 2], 17) ^ rightRotate(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }

    uint32_t a = h[0], b = h[1], c = h[2], d = h[3];
    uint32_t e = h[4], f = h[5], g = h[6], h0 = h[7];

    for (int i = 0; i < 64; ++i) {
        uint32_t S1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25);
        uint32_t ch = (e & f) ^ (~e & g);
        uint32_t temp1 = h0 + S1 + ch + k[i] + w[i];
        uint32_t S0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t temp2 = S0 + maj;

        h0 = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    h[0] += a; h[1] += b; h[2] += c; h[3] += d;
    h[4] += e; h[5] += f; h[6] += g; h[7] += h0;
}

std::vector<std::string> readFileLines(const std::string& filePath) {
    std::vector<std::string> lines;
    std::ifstream file(filePath);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filePath);
    }
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

std::string compareFileContents(const std::string& file1, const std::string& file2) {
    std::vector<std::string> lines1 = readFileLines(file1);
    std::vector<std::string> lines2 = readFileLines(file2);

    std::ostringstream diff;
    diff << "Differences between " << file1 << " and " << file2 << ":\n";

    size_t maxLines = std::max(lines1.size(), lines2.size());
    for (size_t i = 0; i < maxLines; ++i) {
        if (i >= lines1.size()) {
            diff << "Line " << i + 1 << " added in file2: " << lines2[i] << "\n";
        }
        else if (i >= lines2.size()) {
            diff << "Line " << i + 1 << " removed in file2: " << lines1[i] << "\n";
        }
        else if (lines1[i] != lines2[i]) {
            diff << "Line " << i + 1 << " modified:\n";
            diff << "  file1: " << lines1[i] << "\n";
            diff << "  file2: " << lines2[i] << "\n";
        }
    }

    return diff.str();
}

std::vector<uint8_t> SHA256::padMessage(const std::string& message) {
    std::vector<uint8_t> padded(message.begin(), message.end());
    padded.push_back(0x80);

    while (padded.size() % BLOCK_SIZE != 56) {
        padded.push_back(0x00);
    }

    uint64_t bitLength = message.size() * 8;
    for (int i = 7; i >= 0; --i) {
        padded.push_back(static_cast<uint8_t>((bitLength >> (i * 8)) & 0xFF));
    }
    return padded;
}

std::string SHA256::hash(const std::string& input) {
    std::vector<uint8_t> padded = padMessage(input);

    uint32_t h[8] = {
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    };

    for (size_t i = 0; i < padded.size(); i += BLOCK_SIZE) {
        processChunk(padded.data() + i, h);
    }

    std::ostringstream result;
    for (uint32_t value : h) {
        result << std::hex << std::setw(8) << std::setfill('0') << value;
    }

    return result.str();
}

std::string calculateFileHash(const fs::path& filePath) {
    std::ifstream file(filePath, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filePath.string());
    }

    std::ostringstream content;
    content << file.rdbuf();
    return SHA256::hash(content.str());
}


void compareFolders(const std::string& folder1, const std::string& folder2, const std::string& outputReport) {
    std::unordered_map<std::string, std::string> folder1Hashes;
    std::unordered_map<std::string, std::string> folder2Hashes;

    for (const auto& entry : fs::recursive_directory_iterator(folder1)) {
        if (entry.is_regular_file()) {
            std::string relativePath = fs::relative(entry.path(), folder1).string();
            folder1Hashes[relativePath] = calculateFileHash(entry.path());
        }
    }

    for (const auto& entry : fs::recursive_directory_iterator(folder2)) {
        if (entry.is_regular_file()) {
            std::string relativePath = fs::relative(entry.path(), folder2).string();
            folder2Hashes[relativePath] = calculateFileHash(entry.path());
        }
    }

    std::ofstream report(outputReport);
    if (!report.is_open()) {
        throw std::runtime_error("Cannot open report file: " + outputReport);
    }

    report << "Comparison Report\n";
    report << "=================\n";

    for (const auto& [path, hash] : folder2Hashes) {
        if (folder1Hashes.find(path) == folder1Hashes.end()) {
            report << "New file added: " << path << "\n";
        }
        else if (folder1Hashes[path] != hash) {
            report << "File modified: " << path << "\n";
            try {
                report << compareFileContents(folder1 + "/" + path, folder2 + "/" + path) << "\n";
            }
            catch (const std::exception& e) {
                report << "Error comparing files: " << e.what() << "\n";
            }
        }
    }

    for (const auto& [path, hash] : folder1Hashes) {
        if (folder2Hashes.find(path) == folder2Hashes.end()) {
            report << "File removed: " << path << "\n";
        }
    }

    report.close();
    std::cout << "Report generated: " << outputReport << std::endl;
}

std::list<std::string> selectionSort(const std::list<std::string>& inputList) {
    std::list<std::string> sortedList = inputList;
    for (auto it1 = sortedList.begin(); it1 != sortedList.end(); ++it1) {
        auto minIt = it1;
        for (auto it2 = std::next(it1); it2 != sortedList.end(); ++it2) {
            if (*it2 < *minIt) {
                minIt = it2;
            }
        }

        if (minIt != it1) {
            std::swap(*it1, *minIt);
        }
    }

    return sortedList;
}

void moveFolder(const std::string& sourcePath, const std::string& destinationPath) {
    try {
        fs::path source(sourcePath);
        fs::path destination(destinationPath);

        if (!fs::exists(source) || !fs::is_directory(source)) {
            throw std::runtime_error("Source folder does not exist or is not a directory.");
        }

        if (!fs::exists(destination)) {
            fs::create_directories(destination);
        }

        for (const auto& entry : fs::directory_iterator(source)) {
            fs::path target = destination / entry.path().filename();

            if (fs::is_directory(entry)) {
                moveFolder(entry.path().string(), target.string());
            }
            else {
                fs::rename(entry, target);
            }
        }
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}


int main() {
    try {
        std::string folder1 = "C:/Repository/Project1/.vcs/.history/v5";
        std::string folder2 = "C:/Repository/Project1/.vcs/files";
        std::string outputReport = "C:/Users/Vitalya/Desktop/report.txt";

        compareFolders(folder1, folder2, outputReport);
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}


PYBIND11_MODULE(Pybind11Module, m)
{
    m.def("delete_folder", &deleteFolder, "Delete a folder by path");


    py::class_<SHA256>(m, "SHA256")
        .def_static("hash", &SHA256::hash, "Compute SHA256 hash of a string");

    m.def("read_file_lines", &readFileLines, "Read all lines from a file");
    m.def("compare_file_contents", &compareFileContents, "Compare two files line by line");
    m.def("calculate_file_hash", &calculateFileHash, "Calculate SHA256 hash of a file");
    m.def("compare_folders", &compareFolders, "Compare files between two folders and generate a report");
    m.def("selection_sort", &selectionSort, "Sort linked list by string");
    m.def("move_folder", &moveFolder, "just move");
}