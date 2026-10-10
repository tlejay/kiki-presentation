// Lift the foreground subject(s) out of a photo into a transparent PNG.
// Uses Apple Vision (macOS 14+). Usage: swift cutout.swift <input> <output.png>
import AppKit
import CoreImage
import Vision

let args = CommandLine.arguments
guard args.count == 3 else {
  FileHandle.standardError.write("usage: swift cutout.swift <input> <output.png>\n".data(using: .utf8)!)
  exit(2)
}
let inputURL = URL(fileURLWithPath: args[1])
let outputURL = URL(fileURLWithPath: args[2])

guard let ciInput = CIImage(contentsOf: inputURL, options: [.applyOrientationProperty: true]) else {
  FileHandle.standardError.write("cannot read \(args[1])\n".data(using: .utf8)!)
  exit(1)
}
let handler = VNImageRequestHandler(ciImage: ciInput, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let result = request.results?.first else {
  FileHandle.standardError.write("no foreground subject found\n".data(using: .utf8)!)
  exit(1)
}
// croppedToInstancesExtent trims the canvas to the subject's bounding box.
let buffer = try result.generateMaskedImage(
  ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: true)
let ciOutput = CIImage(cvPixelBuffer: buffer)
let context = CIContext()
guard let cg = context.createCGImage(ciOutput, from: ciOutput.extent) else { exit(1) }
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: outputURL)
print("\(outputURL.path) \(cg.width)x\(cg.height) instances=\(result.allInstances.count)")
