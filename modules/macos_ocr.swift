import Foundation
import Vision

guard CommandLine.arguments.count > 1 else {
    fputs("Missing image path\n", stderr)
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let imageURL = URL(fileURLWithPath: imagePath)

guard FileManager.default.fileExists(atPath: imagePath) else {
    fputs("Image file does not exist at \(imagePath)\n", stderr)
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(url: imageURL, options: [:])

do {
    try handler.perform([request])
    let observations = request.results ?? []
    let text = observations
        .compactMap { $0.topCandidates(1).first?.string }
        .joined(separator: "\n")
    print(text)
} catch {
    fputs("OCR failed: \(error.localizedDescription)\n", stderr)
    exit(1)
}
