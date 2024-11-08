#include <fuzzer/FuzzedDataProvider.h>

#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <vector>

// Include necessary headers for GString and PDFCore
#include "GString.h" 
#include "PDFCore.h"

#include "PDFDoc.h"
#include "OutputDev.h"
#include "gmem.h"
#include "gfile.h"

// Derived class to implement pure virtual methods of OutputDev
class MyOutputDev : public OutputDev {
public:
    GBool upsideDown() override { return gFalse; }
    GBool useDrawChar() override { return gFalse; }
    GBool interpretType3Chars() override { return gFalse; }
};

extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    FuzzedDataProvider provider(data, size);

    // Create an OutputDev instance
    MyOutputDev* output_device = new MyOutputDev();

    // Consume parameters for the function
    int page_number = provider.ConsumeIntegral<int>();
    double hdpi = provider.ConsumeFloatingPoint<double>();
    double vdpi = provider.ConsumeFloatingPoint<double>();
    int rotation = provider.ConsumeIntegral<int>();
    GBool use_media_box = provider.ConsumeBool() ? gTrue : gFalse;
    GBool crop = provider.ConsumeBool() ? gTrue : gFalse;
    GBool printing = provider.ConsumeBool() ? gTrue : gFalse;

    // Consume additional integer parameters
    int param1 = provider.ConsumeIntegral<int>();
    int param2 = provider.ConsumeIntegral<int>();
    int param3 = provider.ConsumeIntegral<int>();
    int param4 = provider.ConsumeIntegral<int>();

    // Create a GString for PDFDoc constructor
    GString* fileNameA = new GString("dummy.pdf"); // Use a dummy filename

    // Call the function under test
    PDFDoc pdf_doc(fileNameA); // Using the constructor that requires a GString

    // Check if the PDF document is valid and has pages
    if (pdf_doc.isOk()) {
        int total_pages = pdf_doc.getNumPages(); // Get total number of pages
        if (page_number >= 0 && page_number < total_pages) { // Ensure valid page number
            pdf_doc.displayPageSlice(output_device, page_number, hdpi, vdpi, rotation,
                                      use_media_box, crop, printing, param1, param2,
                                      param3, param4, nullptr, nullptr); // Pass nullptr for abortCheckCbk
        }
    }

    // Cleanup
    delete output_device;
    // No need to delete fileNameA since PDFDoc takes ownership of it

    return 0;
}