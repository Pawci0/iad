#include "Perceptron.h"
#include <algorithm>
#include <boost/numeric/ublas/io.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <iostream>
#include <random>
#define DEBUG 0

namespace ublas = boost::numeric::ublas;

// std::srand(std::time(nullptr));

MultiLayerPerceptron::MultiLayerPerceptron(size_t intputNodes,
                                           size_t hiddenNodes,
                                           size_t outputNodes, int BiasH,
                                           int BiasO,
                                           std::function<double(double)> aF)
    : weigthsIntputHidden(Matrix(hiddenNodes, intputNodes)),
      weigthsHiddenOutput(Matrix(outputNodes, hiddenNodes)),
      biasHidden(Matrix(hiddenNodes, 1, BiasH)),
      biasOutput(Matrix(outputNodes, 1, BiasO)), activationFunction(aF) {

  auto randomMatrix = [](Matrix &m, double min, double max) {
    std::random_device
        rd; // Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<double> dis(min, max);
    for (size_t i = 0; i < m.size1(); i++)
      for (size_t j = 0; j < m.size2(); j++)
        m(i, j) = dis(gen);
  };
  randomMatrix(weigthsHiddenOutput, -1, 1);
  randomMatrix(weigthsIntputHidden, -1, 1);

  if (DEBUG) {
    std::cout << "weigthsHiddenOutput" << weigthsHiddenOutput
              << "\nweigthsIntputHidden" << weigthsIntputHidden << '\n';
  }
}

// assume that given vector is INTPUT_NUMBER X N
Matrix MultiLayerPerceptron::output(Matrix intput) {
  // hidden output
  Matrix hidden = ublas::prod(weigthsIntputHidden, intput);
  if (DEBUG) {
    std::cout << "HIDDEN=weigthsIntputHidden X intput" << '\n'
              << hidden << "\n=\n"
              << weigthsIntputHidden << "\nX\n"
              << intput << "\nHIDDEN+=biasHidden" << hidden << "\n+\n"
              << biasHidden << '\n';
  }

  hidden += biasHidden;

  if (DEBUG) {
    std::cout << "=\n" << hidden << '\n';
  }

  for (size_t i = 0; i < hidden.size1(); i++)
    for (size_t j = 0; j < hidden.size2(); j++)
      hidden(i, j) = activationFunction(hidden(i, j));

  // bad works on copy
  // std::for_each(hidden.data().begin(), hidden.data().end(),
  // activationFunction);
  if (DEBUG) {
    std::cout << "HIDDEN with activationFunction applied to\n"
              << hidden << '\n';
  }
  // output
  Matrix output = ublas::prod(weigthsHiddenOutput, hidden);
  output += biasOutput;
  for (size_t i = 0; i < output.size1(); i++)
    for (size_t j = 0; j < output.size2(); j++)
      output(i, j) = activationFunction(output(i, j));

  return output;
}
