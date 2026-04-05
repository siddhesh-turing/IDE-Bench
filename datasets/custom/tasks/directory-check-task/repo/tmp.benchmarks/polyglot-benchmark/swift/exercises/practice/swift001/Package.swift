// swift-tools-version:5.9.0

import PackageDescription

let package = Package(
  name: "swift001",
  products: [
    .library(
      name: "swift001",
      targets: ["swift001"])
  ],
  dependencies: [],
  targets: [
    .target(
      name: "swift001",
      dependencies: []),
    .testTarget(
      name: "Testswift001",
      dependencies: ["swift001"]),
  ]
)